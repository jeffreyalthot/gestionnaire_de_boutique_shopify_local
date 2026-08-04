from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DiscountDecision:
    allowed: bool
    max_discount_percent: float
    reason: str


class DiscountGuardrails:
    def evaluate(self, sale_price: float, landed_cost: float, requested_percent: float, minimum_margin_percent: float) -> DiscountDecision:
        if sale_price <= 0:
            return DiscountDecision(False, 0.0, "invalid_price")
        maximum_price_reduction = max(0.0, sale_price - landed_cost / max(0.01, 1 - minimum_margin_percent / 100))
        maximum_percent = maximum_price_reduction / sale_price * 100
        allowed = 0 <= requested_percent <= maximum_percent
        return DiscountDecision(allowed, round(maximum_percent, 2), "allowed" if allowed else "margin_guardrail")
