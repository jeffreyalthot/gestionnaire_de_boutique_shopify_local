from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True, slots=True)
class ProfitResult:
    revenue: Decimal
    total_cost: Decimal
    profit: Decimal
    margin_percent: Decimal

    def as_dict(self) -> dict[str, str]:
        return {key: str(value) for key, value in asdict(self).items()}


def profit(revenue: Decimal, *costs: Decimal) -> Decimal:
    return Decimal(str(revenue)) - sum((Decimal(str(cost)) for cost in costs), Decimal("0"))


def profit_result(revenue: Decimal, *costs: Decimal) -> ProfitResult:
    revenue_value = Decimal(str(revenue))
    total_cost = sum((Decimal(str(cost)) for cost in costs), Decimal("0"))
    value = revenue_value - total_cost
    margin = value / revenue_value * Decimal("100") if revenue_value else Decimal("0")
    return ProfitResult(
        revenue_value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        total_cost.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        margin.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
    )
