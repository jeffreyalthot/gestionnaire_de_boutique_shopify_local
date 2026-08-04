from __future__ import annotations

from dataclasses import asdict,dataclass
from decimal import Decimal,ROUND_HALF_UP

@dataclass(frozen=True,slots=True)
class TaxReserveResult:
    collected_cad: Decimal
    refunded_cad: Decimal
    adjustments_cad: Decimal
    payable_cad: Decimal
    reserve_cad: Decimal
    status: str
    def as_dict(self):
        return {k:str(v) if isinstance(v,Decimal) else v for k,v in asdict(self).items()}

class TaxReservePolicy:
    def evaluate(self,tax_collected_cad: object,tax_refunded_cad: object=0,adjustments_cad: object=0,*,buffer_percent: object=0) -> TaxReserveResult:
        collected=max(Decimal("0"),Decimal(str(tax_collected_cad))); refunded=max(Decimal("0"),Decimal(str(tax_refunded_cad))); adjustments=Decimal(str(adjustments_cad))
        payable=max(Decimal("0"),collected-refunded+adjustments)
        reserve=(payable*(Decimal("1")+max(Decimal("0"),Decimal(str(buffer_percent)))/100)).quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)
        return TaxReserveResult(collected,refunded,adjustments,payable,reserve,"funded" if reserve>=payable else "underfunded")

def tax_reserve(tax_collected_cad: float,tax_refunded_cad: float=0.0,adjustments_cad: float=0.0) -> float:
    return float(TaxReservePolicy().evaluate(tax_collected_cad,tax_refunded_cad,adjustments_cad).reserve_cad)
