from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from math import isfinite
from typing import Any, Callable, Iterable, Mapping, Sequence


@dataclass(frozen=True, slots=True)
class HandlerResult:
    topic: str
    action: str
    entity_type: str
    entity_id: str
    payload: dict[str, Any]
    occurred_at: str
    fingerprint: str
    follow_up_operations: tuple[str, ...]
    warnings: tuple[str, ...] = ()
    requires_reconciliation: bool = False
    schema_version: int = 2
    payload_bytes: int = 0
    source_version: str = ""
    shop_domain: str = ""
    event_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class HandlerPolicy:
    maximum_payload_bytes: int = 2_000_000
    maximum_depth: int = 12
    maximum_collection_items: int = 10_000
    maximum_string_length: int = 250_000
    reject_control_characters: bool = True


class WebhookPayloadError(ValueError):
    pass


def _first(payload: Mapping[str, Any], names: Iterable[str]) -> str:
    for name in names:
        value = payload.get(name)
        if value not in (None, ""):
            return str(value)
    return ""


def _utc_timestamp(value: Any) -> tuple[str, bool]:
    if value in (None, ""):
        return datetime.now(timezone.utc).isoformat(), True
    text = str(value).strip()
    try:
        moment = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return datetime.now(timezone.utc).isoformat(), True
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(timezone.utc).isoformat(), False


def _normalize(value: Any, policy: HandlerPolicy, *, depth: int = 0) -> Any:
    if depth > policy.maximum_depth:
        raise WebhookPayloadError("webhook_payload_depth_exceeded")
    if value is None or isinstance(value, (bool, int)):
        return value
    if isinstance(value, float):
        return value if isfinite(value) else None
    if isinstance(value, str):
        if len(value) > policy.maximum_string_length:
            raise WebhookPayloadError("webhook_string_too_large")
        if policy.reject_control_characters and any(ord(character) < 9 or 13 < ord(character) < 32 for character in value):
            raise WebhookPayloadError("webhook_control_character")
        return value
    if isinstance(value, Mapping):
        if len(value) > policy.maximum_collection_items:
            raise WebhookPayloadError("webhook_object_too_large")
        normalized: dict[str, Any] = {}
        for raw_key, raw_value in value.items():
            key = str(raw_key)
            if not key or len(key) > 256:
                raise WebhookPayloadError("webhook_key_invalid")
            normalized[key] = _normalize(raw_value, policy, depth=depth + 1)
        return normalized
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        if len(value) > policy.maximum_collection_items:
            raise WebhookPayloadError("webhook_array_too_large")
        return [_normalize(item, policy, depth=depth + 1) for item in value]
    return str(value)


def _gid_tail(value: str) -> str:
    value = value.strip()
    return value.rsplit("/", 1)[-1] if value.startswith("gid://") else value


def build_result(
    *,
    topic: str,
    action: str,
    payload: dict[str, Any],
    entity_type: str = "resource",
    id_fields: tuple[str, ...] = ("admin_graphql_api_id", "id"),
    follow_ups: tuple[str, ...] = (),
    required: tuple[str, ...] = (),
    headers: Mapping[str, Any] | None = None,
    policy: HandlerPolicy | None = None,
) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise TypeError("payload webhook doit être un objet")
    selected_policy = policy or HandlerPolicy()
    normalized = _normalize(payload, selected_policy)
    canonical_bytes = json.dumps(
        normalized,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
    if len(canonical_bytes) > selected_policy.maximum_payload_bytes:
        raise WebhookPayloadError("webhook_payload_too_large")

    missing = tuple(name for name in required if normalized.get(name) in (None, ""))
    raw_entity_id = _first(normalized, id_fields)
    entity_id = _gid_tail(raw_entity_id)
    occurred, timestamp_warning = _utc_timestamp(
        _first(normalized, ("updated_at", "created_at", "processed_at", "occurred_at"))
    )
    metadata = {str(key).lower(): str(value) for key, value in (headers or {}).items()}
    source_version = metadata.get("x-shopify-api-version", metadata.get("api_version", ""))
    shop_domain = metadata.get("x-shopify-shop-domain", metadata.get("shop_domain", ""))
    event_id = metadata.get("x-shopify-webhook-id", metadata.get("event_id", ""))

    warnings: list[str] = [f"missing:{name}" for name in missing]
    if not entity_id:
        warnings.append("missing:entity_id")
    if timestamp_warning:
        warnings.append("timestamp_defaulted")
    if source_version and len(source_version) > 32:
        warnings.append("api_version_invalid")
    if shop_domain and (len(shop_domain) > 253 or any(character.isspace() for character in shop_domain)):
        warnings.append("shop_domain_invalid")

    unique_followups = tuple(dict.fromkeys(str(item).strip() for item in follow_ups if str(item).strip()))
    fingerprint_material = b"\n".join(
        (
            str(topic).encode("utf-8"),
            str(action).encode("utf-8"),
            str(entity_type).encode("utf-8"),
            entity_id.encode("utf-8"),
            occurred.encode("utf-8"),
            event_id.encode("utf-8"),
            canonical_bytes,
        )
    )
    result = HandlerResult(
        topic=str(topic),
        action=str(action),
        entity_type=str(entity_type),
        entity_id=entity_id,
        payload=dict(normalized),
        occurred_at=occurred,
        fingerprint=hashlib.sha256(fingerprint_material).hexdigest(),
        follow_up_operations=unique_followups,
        warnings=tuple(dict.fromkeys(warnings)),
        requires_reconciliation=bool(missing or not entity_id or timestamp_warning),
        payload_bytes=len(canonical_bytes),
        source_version=source_version,
        shop_domain=shop_domain,
        event_id=event_id,
    )
    return result.to_dict()


def make_handler(
    *,
    topic: str,
    action: str,
    entity_type: str,
    id_fields: tuple[str, ...],
    follow_ups: tuple[str, ...] = (),
    required: tuple[str, ...] = (),
    policy: HandlerPolicy | None = None,
) -> Callable[..., dict[str, Any]]:
    """Fabrique un handler compatible avec l'ancienne signature ``handle(payload)``."""

    def handle(payload: dict[str, Any], headers: Mapping[str, Any] | None = None) -> dict[str, Any]:
        return build_result(
            topic=topic,
            action=action,
            payload=payload,
            entity_type=entity_type,
            id_fields=id_fields,
            follow_ups=follow_ups,
            required=required,
            headers=headers,
            policy=policy,
        )

    handle.__name__ = f"handle_{action}"
    handle.__doc__ = f"Normalise le webhook Shopify {topic}."
    return handle
