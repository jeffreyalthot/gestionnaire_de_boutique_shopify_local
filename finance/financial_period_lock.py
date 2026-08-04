from __future__ import annotations

from datetime import date
from typing import Any


class FinancialPeriodLock:
    def __init__(self, db: Any) -> None:
        self.db = db

    def lock(self, period: str, actor: str) -> None:
        self.db.set_value(f"financial-period:{period}", {"locked": True, "actor": actor, "locked_on": date.today().isoformat()})
        self.db.insert_audit("finance.period.lock", actor, {"period": period})

    def unlock(self, period: str, actor: str, reason: str) -> None:
        if not reason.strip():
            raise ValueError("Une justification est requise.")
        self.db.set_value(f"financial-period:{period}", {"locked": False, "actor": actor, "reason": reason})
        self.db.insert_audit("finance.period.unlock", actor, {"period": period, "reason": reason})

    def is_locked(self, period: str) -> bool:
        return bool(self.db.get_value(f"financial-period:{period}", {}).get("locked", False))
