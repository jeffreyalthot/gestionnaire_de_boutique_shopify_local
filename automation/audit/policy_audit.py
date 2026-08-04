from __future__ import annotations

from typing import Any


class PolicyAudit:
    def __init__(self, db: Any) -> None:
        self.db = db

    def record(self, policy: str, result: dict[str, Any]) -> str:
        return self.db.insert_audit("automation.policy", policy, result)
