from __future__ import annotations

from collections.abc import Mapping, Sequence
from hashlib import sha256
from typing import Any

PII_FIELDS = {
    "email", "phone", "address1", "address2", "zip", "postal_code",
    "first_name", "last_name", "name", "latitude", "longitude",
}


def is_pii_field(name: str) -> bool:
    normalized = str(name).strip().lower().replace("-", "_")
    return normalized in PII_FIELDS or normalized.endswith("_email") or normalized.endswith("_phone")


def minimize_payload(payload: dict[str, object], allow_pii: bool = False) -> dict[str, object]:
    return _minimize(payload, allow_pii=allow_pii)


def _minimize(value: Any, *, allow_pii: bool) -> Any:
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, item in value.items():
            name = str(key)
            if not allow_pii and is_pii_field(name):
                continue
            result[name] = _minimize(item, allow_pii=allow_pii)
        return result
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_minimize(item, allow_pii=allow_pii) for item in value]
    return value


def pseudonymize(value: str, *, salt: str) -> str:
    if not salt:
        raise ValueError("salt is required")
    return sha256(f"{salt}|{value}".encode("utf-8")).hexdigest()


def retention_projection(records: list[dict[str, object]], *, cutoff: str, date_field: str = "created_at") -> dict[str, int]:
    expired = sum(str(item.get(date_field, "")) < cutoff for item in records if item.get(date_field))
    return {"total": len(records), "expired": expired, "retained": len(records) - expired}
