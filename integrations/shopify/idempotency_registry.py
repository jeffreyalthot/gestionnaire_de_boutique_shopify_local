from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any


class ShopifyIdempotencyRegistry:
    def __init__(self, db: Any) -> None:
        self.db = db

    def reserve(self, key: str, operation: str) -> bool:
        now = datetime.now(timezone.utc).isoformat()
        return bool(self.db.execute(
            "INSERT OR IGNORE INTO automation_actions(id,idempotency_key,name,status,result_json,error,updated_at) VALUES(?,?,?,?,?,?,?)",
            (key, key, f"shopify:{operation}", "reserved", "{}", "", now),
        ))

    def complete(self, key: str, result: dict[str, object]) -> bool:
        return bool(self.db.execute(
            "UPDATE automation_actions SET status='completed',result_json=?,error='',updated_at=? WHERE idempotency_key=?",
            (json.dumps(result, ensure_ascii=False, default=str), datetime.now(timezone.utc).isoformat(), key),
        ))

    def fail(self, key: str, error: str, *, retryable: bool = True) -> bool:
        return bool(self.db.execute(
            "UPDATE automation_actions SET status=?,error=?,updated_at=? WHERE idempotency_key=?",
            ("retry" if retryable else "failed", str(error)[:4000], datetime.now(timezone.utc).isoformat(), key),
        ))

    def status(self, key: str) -> str:
        row = self.db.query_one("SELECT status FROM automation_actions WHERE idempotency_key=?", (key,))
        return str(row["status"]) if row else ""

    def result(self, key: str) -> dict[str, object] | None:
        row = self.db.query_one("SELECT result_json FROM automation_actions WHERE idempotency_key=?", (key,))
        return json.loads(row["result_json"]) if row else None
