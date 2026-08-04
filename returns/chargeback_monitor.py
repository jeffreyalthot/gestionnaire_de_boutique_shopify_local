from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class ChargebackExposure:
    cases: int
    amount_cad: float
    disputed_cases: int
    chargeback_cases: int
    reserve_cad: float
    severity: str
    action: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class ChargebackMonitor:
    def __init__(self, db: Any, reserve_ratio: float = 1.15) -> None:
        self.db = db
        self.reserve_ratio = max(1.0, float(reserve_ratio))

    def assess(self) -> ChargebackExposure:
        rows = self.db.query(
            "SELECT status,COUNT(*) count,COALESCE(SUM(amount),0) amount "
            "FROM payments WHERE status IN ('chargeback','disputed') GROUP BY status"
        )
        by_status = {str(row["status"]): row for row in rows}
        cases = sum(int(row["count"]) for row in rows)
        amount = round(sum(float(row["amount"]) for row in rows), 2)
        disputed = int(by_status.get("disputed", {}).get("count", 0))
        chargebacks = int(by_status.get("chargeback", {}).get("count", 0))
        severity = "none" if cases == 0 else "low" if amount < 250 else "medium" if amount < 1_000 else "high"
        action = "none" if cases == 0 else "prepare_evidence" if severity in {"low", "medium"} else "freeze_high_risk_orders"
        return ChargebackExposure(cases, amount, disputed, chargebacks, round(amount * self.reserve_ratio, 2), severity, action)

    def open_exposure(self) -> dict[str, float | int]:
        assessment = self.assess()
        return {"cases": assessment.cases, "amount": assessment.amount_cad}

    def checkpoint(self) -> None:
        self.db.set_value("returns:chargeback_monitor:last_run", datetime.now(timezone.utc).isoformat())

    def run(self) -> ChargebackExposure:
        result = self.assess()
        self.db.set_value("returns:chargeback_monitor:last_result", result.as_dict())
        self.checkpoint()
        return result
