from decimal import Decimal, ROUND_HALF_UP


class CurrencyPresenter:
    SYMBOLS={"CAD":"$","USD":"$ US","EUR":"€"}
    def format(self, amount: float, currency: str="CAD", locale: str="fr-CA") -> str:
        value=Decimal(str(amount)).quantize(Decimal("0.01"),ROUND_HALF_UP); text=f"{value:,.2f}"
        if locale.startswith("fr"): text=text.replace(",","X").replace(".",",").replace("X"," ")
        return f"{text} {self.SYMBOLS.get(currency,currency)}"
