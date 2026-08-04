from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PriceRecheck:
    accepted: bool
    old_cad: float
    new_cad: float
    change_percent: float
    reason: str


class PriceRecheckService:
    def __init__(self, max_increase_percent: float=5.0) -> None: self.max=max(0,max_increase_percent)
    def check(self, old_cad: float, new_cad: float) -> PriceRecheck:
        change=(new_cad-old_cad)/max(0.01,old_cad)*100
        ok=change<=self.max
        return PriceRecheck(ok,old_cad,new_cad,round(change,2),"accepted" if ok else "supplier_price_increase")
