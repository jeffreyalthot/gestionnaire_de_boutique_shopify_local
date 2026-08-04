from __future__ import annotations

from collections import defaultdict
from decimal import Decimal


def optimize_order_sequence(orders: list[dict[str, object]]) -> list[dict[str, object]]:
    """Sort for supplier locality, urgency and descending value."""
    return sorted(
        (dict(order) for order in orders),
        key=lambda item: (
            -int(item.get("priority", 100) == 0),
            str(item.get("supplier_id", "")),
            int(item.get("lead_time_days", 999) or 999),
            -float(item.get("supplier_cost_cad", 0) or 0),
        ),
    )


def optimize_supplier_batches(orders: list[dict[str, object]], *, maximum_batch_cad: Decimal,
                              maximum_orders: int = 100) -> tuple[tuple[dict[str, object], ...], ...]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for order in optimize_order_sequence(orders):
        grouped[str(order.get("supplier_id", "unmapped"))].append(order)
    batches: list[tuple[dict[str, object], ...]] = []
    for supplier in sorted(grouped):
        current: list[dict[str, object]] = []
        total = Decimal("0")
        for order in grouped[supplier]:
            amount = Decimal(str(order.get("supplier_cost_cad", 0) or 0))
            if current and (len(current) >= maximum_orders or total + amount > maximum_batch_cad):
                batches.append(tuple(current)); current = []; total = Decimal("0")
            current.append(order); total += amount
        if current: batches.append(tuple(current))
    return tuple(batches)
