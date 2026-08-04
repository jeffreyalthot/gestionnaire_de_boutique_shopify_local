from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from typing import Any

from ai.memory.long_term_memory import LongTermMemory


class ErrorMemory(LongTermMemory):
    prefix = "error"

    def put(self, key: str, value: object) -> None:
        self.remember(f"{self.prefix}:{key}", value, tags=("error",))

    def get(self, key: str, default: Any = None) -> Any:
        return self.recall(f"{self.prefix}:{key}", default)

    def record_error(
        self,
        message: str,
        *,
        category: str = "runtime",
        severity: str = "error",
        operation: str = "",
        retryable: bool = False,
        context: dict[str, object] | None = None,
    ) -> str:
        fingerprint = sha256(f"{category}|{operation}|{message}".encode("utf-8")).hexdigest()[:24]
        existing = self.get(fingerprint, {})
        count = int(existing.get("count", 0)) + 1 if isinstance(existing, dict) else 1
        now = datetime.now(timezone.utc).isoformat()
        item = {
            "fingerprint": fingerprint,
            "message": str(message)[:2000],
            "category": str(category),
            "severity": str(severity),
            "operation": str(operation),
            "retryable": bool(retryable),
            "context": dict(context or {}),
            "count": count,
            "first_seen_at": existing.get("first_seen_at", now) if isinstance(existing, dict) else now,
            "last_seen_at": now,
            "resolved_at": "",
        }
        self.put(fingerprint, item)
        return fingerprint

    def resolve(self, fingerprint: str) -> bool:
        item = self.get(fingerprint)
        if not isinstance(item, dict):
            return False
        item["resolved_at"] = datetime.now(timezone.utc).isoformat()
        self.put(fingerprint, item)
        return True

    def unresolved(self, limit: int = 100) -> tuple[dict[str, object], ...]:
        values = [
            record.value for record in self.scan(f"{self.prefix}:", limit=limit * 4)
            if isinstance(record.value, dict) and not record.value.get("resolved_at")
        ]
        values.sort(key=lambda item: (str(item.get("severity", "")), str(item.get("last_seen_at", ""))), reverse=True)
        return tuple(values[: max(1, int(limit))])
