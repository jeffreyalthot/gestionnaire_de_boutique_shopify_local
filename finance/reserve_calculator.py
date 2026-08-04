from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True, slots=True)
class ReserveCalculation:
    reserve_type: str
    exposure_cad: Decimal
    base_rate: Decimal
    buffer_rate: Decimal
    reserve_cad: Decimal
    confidence: float
    reason: str

    def as_dict(self) -> dict[str, object]:
        data=asdict(self)
        for key in ("exposure_cad","base_rate","buffer_rate","reserve_cad"): data[key]=str(data[key])
        return data


class ReserveCalculator:
    CENT=Decimal("0.01")
    def calculate(self,reserve_type: str,exposure_cad: object,base_rate: object,*,buffer_rate: object=0,minimum_cad: object=0,maximum_cad: object|None=None,confidence: float=1.0,reason: str="") -> ReserveCalculation:
        exposure=max(Decimal("0"),Decimal(str(exposure_cad))); base=max(Decimal("0"),Decimal(str(base_rate))); buffer=max(Decimal("0"),Decimal(str(buffer_rate)))
        reserve=exposure*base*(Decimal("1")+buffer)
        reserve=max(Decimal(str(minimum_cad)),reserve)
        if maximum_cad is not None: reserve=min(Decimal(str(maximum_cad)),reserve)
        reserve=reserve.quantize(self.CENT,rounding=ROUND_HALF_UP)
        return ReserveCalculation(str(reserve_type),exposure,base,buffer,reserve,max(0.0,min(1.0,float(confidence))),reason or "policy")
