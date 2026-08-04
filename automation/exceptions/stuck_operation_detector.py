from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any


class StuckOperationDetector:
    def __init__(self, db: Any, *, lease_grace_seconds: int = 60) -> None:
        self.db = db
        self.grace = max(0, lease_grace_seconds)

    def detect(self, limit: int = 100) -> list[dict[str, Any]]:
        threshold = (datetime.now(timezone.utc) - timedelta(seconds=self.grace)).isoformat()
        return self.db.query(
            "SELECT id,queue,task_type,attempts,worker_id,lease_until,error FROM tasks "
            "WHERE status='leased' AND lease_until<? ORDER BY lease_until LIMIT ?",
            (threshold, max(1, min(limit, 1000))),
        )
