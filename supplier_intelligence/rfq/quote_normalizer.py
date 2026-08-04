from __future__ import annotations
from dataclasses import asdict,dataclass
from decimal import Decimal,ROUND_HALF_UP

@dataclass(frozen=True,slots=True)
class NormalizedQuote:
    supplier_id: str
    quantity: int
    currency: str
    unit_price_cad: Decimal
    freight_cad: Decimal
    duty_cad: Decimal
    tax_cad: Decimal
    landed_unit_cad: Decimal
    total_cad: Decimal
    lead_time_days: int
    moq: int
    valid: bool
    issues: tuple[str,...]
    def as_dict(self):return {k:str(v) if isinstance(v,Decimal) else v for k,v in asdict(self).items()}

class QuoteNormalizer:
    def normalize(self,q: dict[str,object],rate_to_cad: float=1) -> dict[str,object]:return {**q,**self.evaluate(q,rate_to_cad=rate_to_cad).as_dict()}
    def evaluate(self,q: dict[str,object],*,rate_to_cad: object=1) -> NormalizedQuote:
        rate=Decimal(str(rate_to_cad));qty=max(1,int(q.get("quantity",1) or 1));unit=Decimal(str(q.get("unit_price",0) or 0))*rate;freight=Decimal(str(q.get("freight",0) or 0))*rate;duty=Decimal(str(q.get("duty",0) or 0))*rate;tax=Decimal(str(q.get("tax",0) or 0))*rate;moq=max(1,int(q.get("moq",1) or 1));lead=max(0,int(q.get("lead_time_days",0) or 0));issues=[]
        if unit<=0:issues.append("invalid_unit_price")
        if qty<moq:issues.append("below_moq")
        if rate<=0:issues.append("invalid_exchange_rate")
        total=unit*qty+freight+duty+tax;landed=total/qty;qcent=Decimal("0.01")
        return NormalizedQuote(str(q.get("supplier_id","")),qty,str(q.get("currency","USD")).upper(),unit.quantize(qcent),freight.quantize(qcent),duty.quantize(qcent),tax.quantize(qcent),landed.quantize(qcent,rounding=ROUND_HALF_UP),total.quantize(qcent,rounding=ROUND_HALF_UP),lead,moq,not issues,tuple(issues))
