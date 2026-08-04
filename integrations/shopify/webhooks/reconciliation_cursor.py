from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from infrastructure.database.engine import Database

@dataclass(frozen=True, slots=True)
class ReconciliationWindow:
    start: datetime
    end: datetime
    query_filter: str

class ReconciliationCursor:
    def __init__(self, db: Database, name: str, *, overlap_minutes: int = 5) -> None:
        self.db = db
        self.name = name
        self.overlap = timedelta(minutes=max(0, overlap_minutes))
        self.key = f"shopify.reconciliation.{name}"

    def window(self, *, now: datetime | None = None, default_lookback_hours: int = 24) -> ReconciliationWindow:
        end = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
        raw = self.db.get_value(self.key, None)
        if isinstance(raw, dict) and raw.get("completed_at"):
            try:
                start = datetime.fromisoformat(str(raw["completed_at"]).replace("Z", "+00:00")).astimezone(timezone.utc) - self.overlap
            except ValueError:
                start = end - timedelta(hours=default_lookback_hours)
        else:
            start = end - timedelta(hours=default_lookback_hours)
        return ReconciliationWindow(start, end, f"updated_at:>={start.isoformat()}")

    def commit(self, completed_at: datetime | None = None) -> None:
        stamp = (completed_at or datetime.now(timezone.utc)).astimezone(timezone.utc).isoformat()
        self.db.set_value(self.key, {"completed_at": stamp})
