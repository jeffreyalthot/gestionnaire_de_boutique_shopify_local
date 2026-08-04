from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class RoutedException:
    id: str
    category: str
    severity: str
    retryable: bool
    message: str
    operation: str
    payload: dict[str, Any]
    created_at: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class ExceptionRouter:
    TRANSIENT = (TimeoutError, ConnectionError)

    def classify(self, exc: BaseException, *, operation: str = "", payload: dict[str, Any] | None = None) -> RoutedException:
        text = f"{type(exc).__name__}: {exc}"[:1000]
        lower = text.lower()
        if isinstance(exc, self.TRANSIENT) or any(token in lower for token in ("timeout", "429", "temporar", "connection")):
            category, severity, retryable = "transient", "warning", True
        elif any(token in lower for token in ("auth", "token", "credential", "permission", "401", "403")):
            category, severity, retryable = "authorization", "critical", False
        elif any(token in lower for token in ("validation", "invalid", "schema", "malformed")):
            category, severity, retryable = "data_quality", "error", False
        else:
            category, severity, retryable = "unexpected", "error", False
        return RoutedException(
            str(uuid4()), category, severity, retryable, text, operation,
            dict(payload or {}), datetime.now(timezone.utc).isoformat(),
        )
