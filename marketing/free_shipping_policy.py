from __future__ import annotations
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class FreeShippingDecision:
    eligible: bool
    subsidy_cad: float
    profit_after_shipping_cad: float
    threshold_gap_cad: float
    reason: str
    def as_dict(self):return asdict(self)

class FreeShippingPolicy:
    def eligible(self,*,subtotal_cad: float,shipping_cad: float,gross_profit_cad: float,threshold_cad: float=75) -> bool:return self.evaluate(subtotal_cad=subtotal_cad,shipping_cad=shipping_cad,gross_profit_cad=gross_profit_cad,threshold_cad=threshold_cad).eligible
    def evaluate(self,*,subtotal_cad: float,shipping_cad: float,gross_profit_cad: float,threshold_cad: float=75,minimum_profit_cad: float=3,maximum_subsidy_cad: float|None=None) -> FreeShippingDecision:
        subtotal=max(0,float(subtotal_cad));shipping=max(0,float(shipping_cad));profit=float(gross_profit_cad);subsidy=min(shipping,maximum_subsidy_cad) if maximum_subsidy_cad is not None else shipping;after=profit-subsidy;gap=max(0,float(threshold_cad)-subtotal)
        eligible=gap<=0 and after>=minimum_profit_cad;reason="eligible" if eligible else "threshold_not_met" if gap else "profit_floor"
        return FreeShippingDecision(eligible,round(subsidy,2),round(after,2),round(gap,2),reason)
