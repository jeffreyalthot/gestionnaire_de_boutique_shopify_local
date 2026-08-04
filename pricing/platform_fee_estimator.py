from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True, slots=True)
class FeeEstimate:
    amount: Decimal
    variable_fee: Decimal
    fixed_fee: Decimal
    total_fee: Decimal
    net_amount: Decimal

    def as_dict(self) -> dict[str, object]:
        return {key: str(value) for key, value in asdict(self).items()}


class PlatformFeeEstimator:
    def estimate(self, amount: object, percent: object, fixed: object = 0, *, additional_fees: tuple[object, ...] = ()) -> FeeEstimate:
        value = Decimal(str(amount)); rate = Decimal(str(percent)); fixed_value = Decimal(str(fixed))
        if value < 0 or rate < 0 or fixed_value < 0:
            raise ValueError("frais invalides")
        variable = value * rate / 100
        total = variable + fixed_value + sum((Decimal(str(item)) for item in additional_fees), Decimal("0"))
        total = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return FeeEstimate(value, variable.quantize(Decimal("0.01")), fixed_value, total, (value - total).quantize(Decimal("0.01")))


def estimate_fee(amount: Decimal, percent: Decimal, fixed: Decimal = Decimal("0")) -> Decimal:
    return PlatformFeeEstimator().estimate(amount, percent, fixed).total_fee
