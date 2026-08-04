from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import Any

from app.exception_router import RoutedException


class ExceptionQueue:
    def __init__(self, db: Any) -> None:
        self.db = db

    def push(self, item: RoutedException, *, next_retry_seconds: float | None = None) -> None:
        now = datetime.now(timezone.utc)
        next_retry = (now + timedelta(seconds=max(0.0, next_retry_seconds))).isoformat() if next_retry_seconds is not None else None
        self.db.execute(
            "INSERT OR REPLACE INTO automation_exceptions(id,operation,category,severity,retryable,status,message,payload_json,attempts,next_retry_at,created_at,updated_at) "
            "VALUES(?,?,?,?,?,'open',?,?,0,?,?,?)",
            (item.id, item.operation, item.category, item.severity, int(item.retryable), item.message,
             json.dumps(item.payload, ensure_ascii=False, default=str), next_retry, item.created_at, now.isoformat()),
        )

    def claim_ready(self, limit: int = 50) -> list[dict[str, Any]]:
        now = datetime.now(timezone.utc).isoformat()
        rows = self.db.query(
            "SELECT * FROM automation_exceptions WHERE status='open' AND (next_retry_at IS NULL OR next_retry_at<=?) "
            "ORDER BY CASE severity WHEN 'critical' THEN 0 WHEN 'error' THEN 1 ELSE 2 END, created_at LIMIT ?",
            (now, max(1, min(limit, 500))),
        )
        for row in rows:
            row["payload"] = json.loads(row.pop("payload_json"))
        return rows

    def resolve(self, identifier: str, status: str = "resolved") -> None:
        if status not in {"resolved", "ignored", "escalated", "dead"}:
            raise ValueError("Statut d'exception invalide.")
        self.db.execute("UPDATE automation_exceptions SET status=?,updated_at=? WHERE id=?",
                        (status, datetime.now(timezone.utc).isoformat(), identifier))

    def stats(self) -> dict[str, int]:
        return {str(row["status"]): int(row["count"]) for row in self.db.query(
            "SELECT status,COUNT(*) count FROM automation_exceptions GROUP BY status"
        )}
