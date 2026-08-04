from __future__ import annotations

from datetime import datetime, timedelta, timezone


class RecordRetentionPolicy:
    DEFAULT_DAYS = {"customer_address": 90, "webhook_payload": 30, "audit": 2555, "financial": 2555,
                    "support_message": 730, "media_cache": 30, "temporary": 1}

    def expires_at(self, record_type: str, created_at: datetime, overrides: dict[str, int] | None = None) -> datetime:
        days = (overrides or {}).get(record_type, self.DEFAULT_DAYS.get(record_type, 365))
        return created_at + timedelta(days=max(1, days))

    def expired(self, record_type: str, created_at: datetime, *, now: datetime | None = None,
                overrides: dict[str, int] | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return now >= self.expires_at(record_type, created_at, overrides)
