from __future__ import annotations

from typing import Iterable


class CustomerLifetimeValue:
    def calculate(self, orders: Iterable[dict[str, object]], *, refund_penalty: float = 1.0) -> float:
        total = 0.0
        for order in orders:
            revenue = float(order.get("revenue_cad", order.get("total_amount", 0.0)))
            refunds = float(order.get("refund_cad", 0.0))
            profit = order.get("profit_cad")
            contribution = float(profit) if profit is not None else revenue - refunds * max(0.0, refund_penalty)
            total += contribution
        return round(max(0.0, total), 2)
