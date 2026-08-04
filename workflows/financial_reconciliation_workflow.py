from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from infrastructure.database.engine import Database


class FinancialReconciliationWorkflow:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def execute(self) -> dict[str, object]:
        snapshot = dict(self.db.financial_snapshot())
        ledger = self.db.query_one("SELECT ROUND(SUM(debit),2) debit,ROUND(SUM(credit),2) credit FROM ledger") or {}
        debit = float(ledger.get("debit", 0) or 0)
        credit = float(ledger.get("credit", 0) or 0)
        snapshot.update({
            "ledger_debit": debit,
            "ledger_credit": credit,
            "ledger_balanced": abs(debit - credit) < 0.01,
            "difference": round(debit - credit, 2),
            "reconciled_at": datetime.now(timezone.utc).isoformat(),
        })
        return snapshot
