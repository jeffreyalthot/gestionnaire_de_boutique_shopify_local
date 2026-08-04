from __future__ import annotations

from datetime import datetime, timedelta


class SLAMonitor:
    LIMITS = {"chargeback": 1, "fraud": 1, "lost_package": 4, "damaged_item": 8, "refund": 12, "shipping": 24, "other": 48}

    def due_at(self, created_at: datetime, category: str) -> datetime:
        return created_at + timedelta(hours=self.LIMITS.get(category, 48))

    def breached(self, created_at: datetime, category: str, now: datetime) -> bool:
        return now > self.due_at(created_at, category)
