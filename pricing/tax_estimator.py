from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True, slots=True)
class TaxEstimate:
    taxable_amount: Decimal
    rate_percent: Decimal
    tax: Decimal
    total: Decimal
    inclusive: bool

    def as_dict(self) -> dict[str, object]:
        data = asdict(self)
        return {key: str(value) if isinstance(value, Decimal) else value for key, value in data.items()}


class TaxEstimator:
    def estimate(self, amount: object, percent: object, *, inclusive: bool = False) -> TaxEstimate:
        value = Decimal(str(amount)); rate = Decimal(str(percent))
        if value < 0 or rate < 0:
            raise ValueError("montant ou taxe invalide")
        if inclusive and rate:
            tax = value - value / (Decimal("1") + rate / 100)
            taxable = value - tax
            total = value
        else:
            taxable = value; tax = value * rate / 100; total = value + tax
        q = Decimal("0.01")
        return TaxEstimate(taxable.quantize(q, rounding=ROUND_HALF_UP), rate, tax.quantize(q, rounding=ROUND_HALF_UP), total.quantize(q, rounding=ROUND_HALF_UP), inclusive)


def estimate_taxable_buffer(amount: Decimal, percent: Decimal) -> Decimal:
    return TaxEstimator().estimate(amount, percent).tax
