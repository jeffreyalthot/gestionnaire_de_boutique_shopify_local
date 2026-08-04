from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class CustomerRiskProfile:
    score: float
    level: str
    signals: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class CustomerRiskProfiler:
    def evaluate(self, *, chargebacks: int = 0, refunds: int = 0, orders: int = 0,
                 address_changes: int = 0, failed_payments: int = 0) -> CustomerRiskProfile:
        denominator = max(1, orders)
        signals: list[str] = []
        score = min(1.0, chargebacks * 0.45 + min(0.35, refunds / denominator * 0.5)
                    + min(0.20, failed_payments * 0.05) + min(0.10, address_changes * 0.02))
        if chargebacks:
            signals.append("chargeback_history")
        if refunds / denominator > 0.30:
            signals.append("high_refund_rate")
        if failed_payments >= 3:
            signals.append("payment_failures")
        level = "critical" if score >= 0.75 else ("high" if score >= 0.50 else ("medium" if score >= 0.25 else "low"))
        return CustomerRiskProfile(round(score, 6), level, tuple(signals))
