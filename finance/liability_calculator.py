from __future__ import annotations
from decimal import Decimal
from finance.money_math import sum_money

def total_liabilities(*amounts: object) -> Decimal:
    result = sum_money(amounts)
    if result < 0:
        raise ValueError("Le total des passifs ne peut pas être négatif")
    return result
