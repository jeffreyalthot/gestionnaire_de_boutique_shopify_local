from __future__ import annotations

from typing import Any


class ReconciliationAudit:
    def __init__(self, db: Any) -> None:
        self.db = db

    def record(self, name: str, report: dict[str, Any]) -> str:
        return self.db.insert_audit("automation.reconciliation", name, report)
