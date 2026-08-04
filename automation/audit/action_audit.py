from __future__ import annotations

from typing import Any


class ActionAudit:
    def __init__(self, db: Any) -> None:
        self.db = db

    def record(self, action: str, detail: dict[str, Any], actor: str = "automation") -> str:
        return self.db.insert_audit(action, actor, detail)

    def verify(self) -> dict[str, Any]:
        return self.db.verify_audit_chain()
