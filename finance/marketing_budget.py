from __future__ import annotations


class MarketingBudget:
    def allocate(self, *, available_cash_cad: float, reserve_required_cad: float,
                 trailing_profit_cad: float, maximum_percent_of_profit: float = 0.30) -> dict[str, float | bool]:
        spendable_cash = max(0.0, available_cash_cad - reserve_required_cad)
        profit_limit = max(0.0, trailing_profit_cad) * max(0.0, min(1.0, maximum_percent_of_profit))
        budget = min(spendable_cash, profit_limit)
        return {"budget_cad": round(budget, 2), "reserve_protected": True,
                "cash_limit_cad": round(spendable_cash, 2), "profit_limit_cad": round(profit_limit, 2)}
