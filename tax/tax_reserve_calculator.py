from decimal import Decimal,ROUND_HALF_UP

def _d(v: object)->Decimal:return Decimal(str(v or 0))
def tax_reserve(taxable_sales: float,effective_rate: float,collected_tax: float=0.0,refund_adjustment: float=0.0) -> float:
    reserve=max(Decimal("0"),_d(taxable_sales)*max(Decimal("0"),_d(effective_rate))-_d(collected_tax)-_d(refund_adjustment))
    return float(reserve.quantize(Decimal("0.01"),rounding=ROUND_HALF_UP))
class TaxReserveCalculator:
    def calculate(self,**kwargs) -> dict[str,object]:
        value=tax_reserve(**kwargs);return {"reserve_cad":value,"funded":value<=0,"inputs":dict(kwargs)}
