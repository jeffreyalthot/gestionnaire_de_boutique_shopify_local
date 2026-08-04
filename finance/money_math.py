from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable

CENT = Decimal("0.01")
HUNDRED = Decimal("100")


def decimal_money(value: object) -> Decimal:
    try:
        amount = Decimal(str(value))
    except Exception as exc:
        raise ValueError(f"Montant invalide: {value!r}") from exc
    if not amount.is_finite():
        raise ValueError("Le montant doit être fini")
    return amount.quantize(CENT, rounding=ROUND_HALF_UP)


def percentage(value: object) -> Decimal:
    result = Decimal(str(value))
    if not result.is_finite():
        raise ValueError("Le pourcentage doit être fini")
    return result


def percent_of(amount: object, rate_percent: object) -> Decimal:
    return (decimal_money(amount) * percentage(rate_percent) / HUNDRED).quantize(CENT, rounding=ROUND_HALF_UP)


@dataclass(frozen=True, slots=True)
class ProfitBreakdown:
    revenue: Decimal
    cost_of_goods: Decimal
    shipping: Decimal
    platform_fees: Decimal
    marketing: Decimal
    refunds: Decimal
    taxes: Decimal
    other_expenses: Decimal
    gross_profit: Decimal
    net_profit: Decimal
    gross_margin_percent: Decimal
    net_margin_percent: Decimal


def profit_breakdown(
    revenue: object,
    *,
    cost_of_goods: object = 0,
    shipping: object = 0,
    platform_fees: object = 0,
    marketing: object = 0,
    refunds: object = 0,
    taxes: object = 0,
    other_expenses: object = 0,
) -> ProfitBreakdown:
    rev = decimal_money(revenue)
    values = [decimal_money(v) for v in (cost_of_goods, shipping, platform_fees, marketing, refunds, taxes, other_expenses)]
    if rev < 0 or any(value < 0 for value in values):
        raise ValueError("Les revenus et dépenses ne peuvent pas être négatifs")
    cogs, ship, fees, ads, refund, tax, other = values
    gross = rev - cogs - ship
    net = gross - fees - ads - refund - tax - other
    gross_margin = (gross / rev * HUNDRED).quantize(CENT, rounding=ROUND_HALF_UP) if rev else Decimal("0.00")
    net_margin = (net / rev * HUNDRED).quantize(CENT, rounding=ROUND_HALF_UP) if rev else Decimal("0.00")
    return ProfitBreakdown(rev, cogs, ship, fees, ads, refund, tax, other, gross, net, gross_margin, net_margin)


def sum_money(values: Iterable[object]) -> Decimal:
    return sum((decimal_money(value) for value in values), start=Decimal("0.00")).quantize(CENT)
