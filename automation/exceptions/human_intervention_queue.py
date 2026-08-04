from __future__ import annotations

from typing import Any


class HumanInterventionQueue:
    def __init__(self, db: Any) -> None:
        self.db = db

    def request(self, *, action: str, entity_type: str, entity_id: str, amount_cad: float = 0.0, reason: str = "") -> str:
        from uuid import uuid4
        from infrastructure.database.engine import utcnow
        identifier = str(uuid4())
        self.db.execute(
            "INSERT INTO approvals(id,action,entity_type,entity_id,amount_cad,status,requested_at,reason) "
            "VALUES(?,?,?,?,?,'pending',?,?)",
            (identifier, action, entity_type, entity_id, max(0.0, amount_cad), utcnow(), reason[:1000]),
        )
        return identifier

    def pending(self, limit: int = 100) -> list[dict[str, Any]]:
        return self.db.query("SELECT * FROM approvals WHERE status='pending' ORDER BY requested_at LIMIT ?", (max(1, min(limit, 1000)),))
