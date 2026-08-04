from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class ShippingSubsidyDecision:
    maximum_cad: float
    requested_cad: float
    approved_cad: float
    allowed: bool
    reason: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class ShippingSubsidyPolicy:
    def maximum(self, *, order_value_cad: float, gross_profit_cad: float, max_percent_of_profit: float = 30) -> float:
        return self.evaluate(order_value_cad=order_value_cad, gross_profit_cad=gross_profit_cad, requested_cad=0, max_percent_of_profit=max_percent_of_profit).maximum_cad

    def evaluate(self, *, order_value_cad: float, gross_profit_cad: float, requested_cad: float, max_percent_of_profit: float = 30, maximum_percent_of_order: float = 10) -> ShippingSubsidyDecision:
        order = max(0.0, float(order_value_cad)); profit = max(0.0, float(gross_profit_cad))
        maximum = round(max(0.0, min(order * maximum_percent_of_order / 100, profit * max_percent_of_profit / 100)), 2)
        requested = max(0.0, float(requested_cad))
        approved = round(min(requested, maximum), 2)
        return ShippingSubsidyDecision(maximum, requested, approved, requested <= maximum, "within_budget" if requested <= maximum else "capped_by_profit")
