from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from time import monotonic
from typing import Any, ClassVar, Mapping

from integrations.alibaba.gateway import AlibabaGateway


@dataclass(frozen=True, slots=True)
class AlibabaMethodStats:
    method: str
    calls: int
    successes: int
    failures: int
    total_seconds: float
    last_duration_ms: float
    last_called_at: str
    last_request_fingerprint: str
    last_error: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class AlibabaMethod:
    """Validated Alibaba gateway method preserving the historical execute API."""

    method: ClassVar[str] = ""
    category: ClassVar[str] = "general"
    mutating: ClassVar[bool] = False
    session_required: ClassVar[bool] = True
    required_fields: ClassVar[tuple[str, ...]] = ()
    maximum_fields: ClassVar[int] = 128
    maximum_serialized_bytes: ClassVar[int] = 256 * 1024

    def __init__(self, gateway: AlibabaGateway) -> None:
        self.gateway = gateway
        self.calls = 0
        self.successes = 0
        self.failures = 0
        self.total_seconds = 0.0
        self.last_duration_ms = 0.0
        self.last_called_at = ""
        self.last_request_fingerprint = ""
        self.last_error = ""

    async def execute(self, **params: object) -> dict[str, object]:
        normalized = self.validate_params(params)
        started = monotonic()
        self.calls += 1
        self.last_called_at = datetime.now(timezone.utc).isoformat()
        self.last_request_fingerprint = self.fingerprint(normalized)
        try:
            payload = await self.gateway.call(
                self.method,
                normalized,
                session_required=self.session_required,
            )
            if not isinstance(payload, dict):
                raise TypeError("La passerelle Alibaba doit retourner un objet JSON.")
            self.successes += 1
            self.last_error = ""
            return payload
        except Exception as exc:
            self.failures += 1
            self.last_error = f"{type(exc).__name__}: {exc}"[:1000]
            raise
        finally:
            elapsed = monotonic() - started
            self.total_seconds += elapsed
            self.last_duration_ms = round(elapsed * 1000, 3)

    def validate_params(self, params: Mapping[str, object]) -> dict[str, object]:
        if not self.method:
            raise ValueError("Méthode Alibaba non configurée.")
        if len(params) > self.maximum_fields:
            raise ValueError("Trop de paramètres Alibaba.")
        normalized = {str(key).strip(): self._normalize(value) for key, value in params.items() if value is not None}
        if any(not key for key in normalized):
            raise ValueError("Nom de paramètre Alibaba vide.")
        missing = [field for field in self.required_fields if field not in normalized or normalized[field] in {"", (), [], {}}]
        if missing:
            raise ValueError("Paramètres Alibaba requis absents: " + ", ".join(missing))
        serialized = json.dumps(normalized, ensure_ascii=False, default=str, separators=(",", ":"))
        if len(serialized.encode("utf-8")) > self.maximum_serialized_bytes:
            raise ValueError("Paramètres Alibaba trop volumineux.")
        return normalized

    @classmethod
    def _normalize(cls, value: object) -> object:
        if isinstance(value, Mapping):
            return {str(key): cls._normalize(item) for key, item in value.items() if item is not None}
        if isinstance(value, (list, tuple, set)):
            return [cls._normalize(item) for item in value]
        if isinstance(value, str):
            return value.strip()
        return value

    @staticmethod
    def fingerprint(params: Mapping[str, object]) -> str:
        payload = json.dumps(params, ensure_ascii=False, default=str, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]

    def stats(self) -> AlibabaMethodStats:
        return AlibabaMethodStats(
            self.method,
            self.calls,
            self.successes,
            self.failures,
            round(self.total_seconds, 6),
            self.last_duration_ms,
            self.last_called_at,
            self.last_request_fingerprint,
            self.last_error,
        )

    def describe(self) -> dict[str, object]:
        return {
            "method": self.method,
            "category": self.category,
            "mutating": self.mutating,
            "session_required": self.session_required,
            "required_fields": self.required_fields,
            "limits": {"fields": self.maximum_fields, "serialized_bytes": self.maximum_serialized_bytes},
            "stats": self.stats().as_dict(),
        }
