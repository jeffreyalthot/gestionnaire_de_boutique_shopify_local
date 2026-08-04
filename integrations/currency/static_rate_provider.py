from decimal import Decimal
class StaticRateProvider:
    def __init__(self,rates: dict[tuple[str,str],Decimal]|None=None) -> None:
        self.rates=rates or {("USD","CAD"):Decimal("1.36"),("CAD","USD"):Decimal("0.735294")}
    async def rate(self,source: str,target: str) -> Decimal:
        if source==target: return Decimal("1")
        key=(source,target)
        if key not in self.rates: raise KeyError(f"Taux absent: {source}/{target}")
        return self.rates[key]
