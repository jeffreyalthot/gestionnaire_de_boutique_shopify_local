from __future__ import annotations


def calculate_priority(category: str, *, order_value: float = 0.0, waiting_hours: float = 0.0, vip: bool = False) -> int:
    base = {"chargeback": 5, "fraud": 10, "lost_package": 20, "damaged_item": 30, "refund": 40, "cancellation": 45, "shipping": 60}.get(category, 100)
    base -= 10 if vip else 0
    base -= min(20, int(waiting_hours // 6) * 2)
    base -= 5 if order_value >= 500 else 0
    return max(1, base)
