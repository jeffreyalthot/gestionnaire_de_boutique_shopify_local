from __future__ import annotations
from finance.money_math import ProfitBreakdown, profit_breakdown

def calculate_gross_profit(revenue: object, cost_of_goods: object, shipping: object = 0) -> ProfitBreakdown:
    return profit_breakdown(revenue, cost_of_goods=cost_of_goods, shipping=shipping)
def gross_profit(revenue: float, cost_of_goods: float, shipping: float = 0) -> float:
    return float(calculate_gross_profit(revenue, cost_of_goods, shipping).gross_profit)
