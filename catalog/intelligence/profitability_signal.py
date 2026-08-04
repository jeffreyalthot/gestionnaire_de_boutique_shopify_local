from __future__ import annotations


def profitability_signal(sale_price: float, landed_cost: float, reserve: float = 0.0) -> float:
    if sale_price <= 0:
        return 0.0
    margin = (sale_price - landed_cost - reserve) / sale_price
    return max(0.0, min(1.0, margin / 0.60))
