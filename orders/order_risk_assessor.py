from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class OrderRisk:
    score: float
    level: str
    hold: bool
    reasons: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class OrderRiskAssessor:
    def assess(self, order: dict[str, object]) -> OrderRisk:
        score = 0.0
        reasons: list[str] = []
        amount = float(order.get("amount", order.get("total_amount", 0)) or 0)
        if amount >= 500:
            score += min(0.35, amount / 5000)
            reasons.append("high_value")
        if bool(order.get("billing_shipping_mismatch")):
            score += 0.20; reasons.append("address_mismatch")
        velocity = int(order.get("orders_last_hour", 0) or 0)
        if velocity >= 3:
            score += min(0.30, velocity * 0.05); reasons.append("velocity")
        if bool(order.get("proxy_or_vpn")):
            score += 0.12; reasons.append("proxy")
        if bool(order.get("high_risk_country")):
            score += 0.20; reasons.append("country_risk")
        if bool(order.get("payment_failed_before")):
            score += 0.10; reasons.append("payment_history")
        score = min(1.0, score)
        level = "low" if score < 0.25 else "medium" if score < 0.50 else "high" if score < 0.75 else "critical"
        return OrderRisk(round(score, 4), level, score >= 0.50, tuple(reasons))
