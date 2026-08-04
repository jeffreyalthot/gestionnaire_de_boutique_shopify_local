from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FreightRequote:
    accepted: bool
    original_cad: float
    quoted_cad: float
    reason: str


class FreightRequoteService:
    def __init__(self, max_increase_cad: float=5, max_increase_percent: float=15) -> None: self.max_abs=max_increase_cad; self.max_pct=max_increase_percent
    def check(self, original_cad: float, quoted_cad: float) -> FreightRequote:
        delta=quoted_cad-original_cad; pct=delta/max(.01,original_cad)*100
        ok=delta<=self.max_abs and pct<=self.max_pct
        return FreightRequote(ok,original_cad,quoted_cad,"accepted" if ok else "freight_increase")
