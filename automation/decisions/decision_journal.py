from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


class DecisionJournal:
    def __init__(self, db: Any) -> None:
        self.db = db

    def record(self, *, policy: str, entity_type: str, entity_id: str, allowed: bool,
               score: float, reason: str, detail: dict[str, Any] | None = None) -> str:
        identifier = str(uuid4())
        self.db.execute(
            "INSERT INTO policy_decisions(id,policy,entity_type,entity_id,allowed,score,reason,detail_json,created_at) "
            "VALUES(?,?,?,?,?,?,?,?,?)",
            (identifier, policy, entity_type, entity_id, int(allowed), float(score), reason,
             json.dumps(detail or {}, ensure_ascii=False, default=str), datetime.now(timezone.utc).isoformat()),
        )
        return identifier

    def recent(self, limit: int = 100) -> list[dict[str, Any]]:
        rows = self.db.query("SELECT * FROM policy_decisions ORDER BY created_at DESC LIMIT ?", (max(1, min(limit, 1000)),))
        for row in rows:
            row["detail"] = json.loads(row.pop("detail_json"))
        return rows
