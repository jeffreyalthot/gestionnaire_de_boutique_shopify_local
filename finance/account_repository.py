from __future__ import annotations

from typing import Any


class AccountRepository:
    def __init__(self, db: Any) -> None:
        self.db = db

    def balance(self, account: str, currency: str = "CAD") -> float:
        row = self.db.query_one(
            "SELECT COALESCE(SUM(debit),0) debit,COALESCE(SUM(credit),0) credit FROM ledger WHERE account=? AND currency=?",
            (account, currency),
        ) or {"debit": 0, "credit": 0}
        return round(float(row["debit"]) - float(row["credit"]), 2)

    def trial_balance(self, currency: str = "CAD") -> list[dict[str, object]]:
        rows = self.db.query(
            "SELECT account,COALESCE(SUM(debit),0) debit,COALESCE(SUM(credit),0) credit FROM ledger WHERE currency=? GROUP BY account ORDER BY account",
            (currency,),
        )
        return [{**row, "balance": round(float(row["debit"]) - float(row["credit"]), 2)} for row in rows]
