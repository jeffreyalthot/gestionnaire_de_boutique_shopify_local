from __future__ import annotations

from risk.risk_score import RiskScore


class OrderFraudRules:
    DEFAULT_WEIGHTS = {
        "proxy_or_vpn": .15,
        "billing_shipping_mismatch": .20,
        "disposable_email": .15,
        "high_risk_country": .20,
        "velocity_exceeded": .20,
        "failed_payment_attempts": .12,
        "email_name_mismatch": .08,
        "unverified_phone": .06,
        "forwarding_address": .12,
    }

    def __init__(self, weights: dict[str, float] | None = None) -> None:
        self.weights = {**self.DEFAULT_WEIGHTS, **(weights or {})}

    def assess(self, order: dict[str, object]) -> RiskScore:
        score = 0.0
        reasons: list[str] = []
        factors: dict[str, float] = {}
        aliases = {
            "billing_shipping_mismatch": "address_mismatch",
            "high_risk_country": "country_risk",
            "proxy_or_vpn": "proxy",
        }
        for name, weight in self.weights.items():
            raw = order.get(name)
            active = bool(raw)
            if isinstance(raw, (int, float)) and not isinstance(raw, bool):
                active = float(raw) > 0
            if active:
                contribution = min(float(weight) * (max(1.0, float(raw)) if isinstance(raw, (int, float)) and not isinstance(raw, bool) else 1.0), .35)
                score += contribution
                factors[name] = contribution
                reasons.append(aliases.get(name, name))
        amount = float(order.get("total_amount", order.get("total_price", 0)) or 0)
        if amount >= 750:
            contribution = min(.3, amount / 5000)
            score += contribution
            factors["high_value"] = contribution
            reasons.append("high_value")
        account_age = float(order.get("account_age_days", 0) or 0)
        if account_age < 1 and amount >= 250:
            score += .12; factors["new_account_high_value"] = .12; reasons.append("new_account_high_value")
        history_orders = int(order.get("customer_order_count", 0) or 0)
        history_chargebacks = int(order.get("customer_chargebacks", 0) or 0)
        if history_chargebacks:
            contribution = min(.35, history_chargebacks * .18)
            score += contribution; factors["chargeback_history"] = contribution; reasons.append("chargeback_history")
        if history_orders >= 5 and history_chargebacks == 0:
            score -= .08; factors["trusted_history"] = -.08
        evidence_count = sum(1 for value in factors.values() if value > 0)
        confidence = min(1.0, .45 + evidence_count * .08)
        return RiskScore.build(score, reasons, factors=factors, confidence=confidence)
