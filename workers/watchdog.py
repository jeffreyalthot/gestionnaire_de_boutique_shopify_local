from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from infrastructure.database.engine import Database


class Watchdog:
    def __init__(self, db: Database, *, dead_limit: int = 1000) -> None:
        self.db = db
        self.dead_limit = max(1, int(dead_limit))
        self.runs = 0

    def recover(self) -> dict[str, int | str | bool]:
        expired = int(self.db.purge_expired_leases() or 0)
        dead = int(self.db.scalar("SELECT COUNT(*) FROM tasks WHERE status='dead'", default=0) or 0)
        stuck = int(self.db.scalar("SELECT COUNT(*) FROM tasks WHERE status='leased' AND lease_until<datetime('now')", default=0) or 0)
        self.runs += 1
        return {
            "expired_leases": expired,
            "dead_tasks": dead,
            "stuck_leases": stuck,
            "healthy": dead < self.dead_limit and stuck == 0,
            "runs": self.runs,
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }
