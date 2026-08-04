from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExchangePlan:
    allowed: bool
    replacement_sku: str
    quantity: int
    incremental_cost_cad: float
    reason: str


class ExchangePlanner:
    def plan(self, *, replacement_sku: str, quantity: int, stock_available: int,
             outbound_cost_cad: float, return_cost_cad: float, budget_cad: float) -> ExchangePlan:
        if quantity <= 0:
            return ExchangePlan(False, replacement_sku, quantity, 0.0, 'invalid_quantity')
        cost = round(outbound_cost_cad + return_cost_cad, 2)
        if stock_available < quantity:
            return ExchangePlan(False, replacement_sku, quantity, cost, 'insufficient_stock')
        if cost > budget_cad:
            return ExchangePlan(False, replacement_sku, quantity, cost, 'budget_exceeded')
        return ExchangePlan(True, replacement_sku, quantity, cost, 'approved')
