from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True, slots=True)
class MarkupCalculation:
    cost: Decimal
    markup_percent: Decimal
    price: Decimal
    profit: Decimal
    margin_percent: Decimal

    def as_dict(self) -> dict[str, object]:
        return {key: str(value) for key, value in asdict(self).items()}


class MarkupCalculator:
    CENT = Decimal("0.01")

    def calculate(self, cost: object, markup_percent: object) -> MarkupCalculation:
        c = Decimal(str(cost)); markup = Decimal(str(markup_percent))
        if c < 0 or markup < -100:
            raise ValueError("coût ou markup invalide")
        price = (c * (Decimal("1") + markup / 100)).quantize(self.CENT, rounding=ROUND_HALF_UP)
        profit = (price - c).quantize(self.CENT, rounding=ROUND_HALF_UP)
        margin = (profit / price * 100).quantize(self.CENT, rounding=ROUND_HALF_UP) if price else Decimal("0")
        return MarkupCalculation(c.quantize(self.CENT), markup, price, profit, margin)


def sale_price_for_markup(cost: Decimal, markup_percent: Decimal) -> Decimal:
    return MarkupCalculator().calculate(cost, markup_percent).price
