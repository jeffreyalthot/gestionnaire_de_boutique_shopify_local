from __future__ import annotations
from finance.money_math import ProfitBreakdown, profit_breakdown, sum_money

def calculate_net_profit(revenue: object, *expenses: object) -> ProfitBreakdown:
    return profit_breakdown(revenue, other_expenses=sum_money(expenses))
def net_profit(revenue: float, *expenses: float) -> float:
    return float(calculate_net_profit(revenue, *expenses).net_profit)
