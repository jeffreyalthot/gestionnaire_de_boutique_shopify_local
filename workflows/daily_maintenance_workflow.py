from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from compliance.customer_data_retention import purge_expired_addresses
from infrastructure.database.backup import backup_database


class DailyMaintenanceWorkflow:
    def __init__(self, db: Any, retention_days: int) -> None:
        self.db = db
        self.retention_days = max(1, int(retention_days))
        self.runs = 0

    async def execute(self, *, vacuum: bool = False) -> dict[str, object]:
        backup = backup_database(self.db)
        purged = purge_expired_addresses(self.db, self.retention_days)
        integrity = self.db.query_one("PRAGMA quick_check")
        vacuumed = False
        if vacuum:
            self.db.execute("PRAGMA optimize")
            vacuumed = True
        self.runs += 1
        return {
            "backup": str(backup),
            "addresses_purged": int(purged or 0),
            "integrity": dict(integrity or {}),
            "optimized": vacuumed,
            "runs": self.runs,
            "completed_at": datetime.now(timezone.utc).isoformat(),
        }
