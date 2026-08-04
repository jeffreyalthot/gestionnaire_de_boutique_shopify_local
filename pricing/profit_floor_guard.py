from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProfitFloorDecision:
    allowed: bool
    profit_cad: float
    margin_percent: float
    reason: str


class ProfitFloorGuard:
    def __init__(self, min_profit_cad: float=3.0, min_margin_percent: float=20.0) -> None:
        self.min_profit=min_profit_cad; self.min_margin=min_margin_percent
    def evaluate(self, *, price_cad: float, landed_cost_cad: float, fees_cad: float=0.0, tax_cad: float=0.0) -> ProfitFloorDecision:
        profit=round(price_cad-landed_cost_cad-fees_cad-tax_cad,2); margin=round(profit/max(0.01,price_cad)*100,2)
        if profit<self.min_profit: return ProfitFloorDecision(False,profit,margin,"profit_below_floor")
        if margin<self.min_margin: return ProfitFloorDecision(False,profit,margin,"margin_below_floor")
        return ProfitFloorDecision(True,profit,margin,"allowed")
