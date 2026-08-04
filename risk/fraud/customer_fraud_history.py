from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class CustomerFraudAssessment:
    score: float
    level: str
    hold: bool
    reasons: tuple[str, ...]
    chargeback_rate: float
    failed_payment_rate: float

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class CustomerFraudHistory:
    def assess(
        self,
        *,
        chargebacks: int,
        failed_payments: int,
        total_orders: int,
        account_age_days: int = 0,
        refunds: int = 0,
    ) -> CustomerFraudAssessment:
        orders = max(0, int(total_orders))
        chargeback_count = max(0, int(chargebacks))
        failed_count = max(0, int(failed_payments))
        refund_count = max(0, int(refunds))
        chargeback_rate = chargeback_count / max(1, orders)
        failed_rate = failed_count / max(1, orders + failed_count)
        score = min(1.0, chargeback_rate * 3.5 + failed_rate * 0.9 + min(0.3, refund_count / max(1, orders) * 0.4))
        reasons: list[str] = []
        if chargeback_count:
            reasons.append("chargeback_history")
        if failed_rate >= 0.3:
            reasons.append("high_failed_payment_rate")
        if account_age_days < 7 and orders <= 1:
            score = min(1.0, score + 0.08)
            reasons.append("new_customer")
        level = "low" if score < 0.25 else "medium" if score < 0.55 else "high" if score < 0.8 else "critical"
        return CustomerFraudAssessment(round(score, 4), level, score >= 0.55, tuple(reasons), round(chargeback_rate, 4), round(failed_rate, 4))

    def score(self, *, chargebacks: int, failed_payments: int, total_orders: int) -> float:
        return self.assess(chargebacks=chargebacks, failed_payments=failed_payments, total_orders=total_orders).score
