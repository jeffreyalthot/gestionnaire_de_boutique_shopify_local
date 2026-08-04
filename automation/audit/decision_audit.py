from __future__ import annotations

from typing import Any


class DecisionAudit:
    def __init__(self, db: Any) -> None:
        self.db = db

    def record(self, decision: dict[str, Any], *, actor: str = "decision-engine") -> str:
        return self.db.insert_audit("automation.decision", actor, decision)
