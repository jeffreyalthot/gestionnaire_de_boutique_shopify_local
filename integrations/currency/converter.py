from decimal import Decimal
class CurrencyConverter:
    def __init__(self,provider) -> None: self.provider=provider
    async def convert(self,amount: Decimal,source: str,target: str) -> Decimal:
        if source==target: return Decimal(str(amount))
        rate=Decimal(str(await self.provider.rate(source,target)))
        return Decimal(str(amount))*rate
