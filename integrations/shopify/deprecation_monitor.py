from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
from typing import Mapping


class DeprecationMonitor:
    HEADERS = ("X-Shopify-API-Deprecated-Reason", "X-Shopify-API-Deprecation-Info")

    def __init__(self, history_size: int = 100) -> None:
        self._history: deque[dict[str, str]] = deque(maxlen=max(1, int(history_size)))

    def inspect(self, headers: Mapping[str, object], *, operation: str = "") -> dict[str, str]:
        normalized = {str(key).lower(): str(value) for key, value in headers.items()}
        values = {
            header: normalized[header.lower()]
            for header in self.HEADERS if header.lower() in normalized
        }
        if values:
            values["operation"] = operation
            values["observed_at"] = datetime.now(timezone.utc).isoformat()
            self._history.append(dict(values))
        return values

    def history(self) -> tuple[dict[str, str], ...]:
        return tuple(dict(item) for item in self._history)

    def snapshot(self) -> dict[str, object]:
        return {"count": len(self._history), "last": dict(self._history[-1]) if self._history else None}
