from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from finance.money_math import decimal_money, percent_of
@dataclass(frozen=True, slots=True)
class RefundReserveDecision:
    revenue: Decimal
    rate_percent: Decimal
    reserve: Decimal
    available_after_reserve: Decimal

def calculate_refund_reserve(revenue: object, percent: object, *, minimum: object = 0, maximum: object | None = None) -> RefundReserveDecision:
    rev = decimal_money(revenue)
    rate = Decimal(str(percent))
    if rev < 0 or rate < 0 or rate > 100:
        raise ValueError("Revenu ou taux de réserve invalide")
    reserve = max(decimal_money(minimum), percent_of(rev, rate))
    if maximum is not None:
        reserve = min(reserve, decimal_money(maximum))
    reserve = min(reserve, rev)
    return RefundReserveDecision(rev, rate, reserve, rev - reserve)
def reserve_amount(revenue: float, percent: float) -> float:
    return float(calculate_refund_reserve(revenue, percent).reserve)
