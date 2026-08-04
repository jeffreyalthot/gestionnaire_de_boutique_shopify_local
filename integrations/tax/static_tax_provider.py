from decimal import Decimal, ROUND_HALF_UP
from integrations.tax.tax_provider import TaxProvider, TaxQuote


class StaticTaxProvider(TaxProvider):
    def __init__(self, rates: dict[str, float] | None = None) -> None:
        self.rates = rates or {}

    async def quote(self, subtotal: float, country: str, province: str = "", currency: str = "CAD") -> TaxQuote:
        rate = Decimal(str(self.rates.get(f"{country}:{province}", self.rates.get(country, 0))))
        base = Decimal(str(subtotal))
        tax = (base * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        total = (base + tax).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return TaxQuote(float(base), float(tax), float(total), currency, "static")
