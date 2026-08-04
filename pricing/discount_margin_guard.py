from __future__ import annotations

from dataclasses import asdict, dataclass

from pricing.profit_floor_guard import ProfitFloorDecision, ProfitFloorGuard


@dataclass(frozen=True, slots=True)
class DiscountDecision:
    allowed: bool
    requested_percent: float
    applied_percent: float
    sale_price_cad: float
    floor: ProfitFloorDecision
    reasons: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["floor"] = self.floor.__dict__ if hasattr(self.floor, "__dict__") else str(self.floor)
        return data


class DiscountMarginGuard:
    def __init__(self, floor: ProfitFloorGuard | None = None) -> None:
        self.floor = floor or ProfitFloorGuard()

    def evaluate(self, *, regular_price_cad: float, discount_percent: float, landed_cost_cad: float, fees_cad: float = 0) -> ProfitFloorDecision:
        return self.plan(regular_price_cad=regular_price_cad, discount_percent=discount_percent, landed_cost_cad=landed_cost_cad, fees_cad=fees_cad).floor

    def plan(self, *, regular_price_cad: float, discount_percent: float, landed_cost_cad: float, fees_cad: float = 0, maximum_discount_percent: float = 70) -> DiscountDecision:
        if regular_price_cad <= 0:
            raise ValueError("prix régulier invalide")
        requested = max(0.0, min(100.0, float(discount_percent)))
        applied = min(requested, max(0.0, float(maximum_discount_percent)))
        price = round(float(regular_price_cad) * (1 - applied / 100), 2)
        floor = self.floor.evaluate(price_cad=price, landed_cost_cad=landed_cost_cad, fees_cad=fees_cad)
        reasons: list[str] = []
        if requested > maximum_discount_percent:
            reasons.append("discount_capped")
        if not floor.allowed:
            reasons.append("profit_floor_blocked")
        return DiscountDecision(bool(floor.allowed), requested, applied, price, floor, tuple(reasons))
