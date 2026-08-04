from __future__ import annotations

from ai.features.base import age_hours, as_float, bounded, safe_ratio


def order_features(order: dict[str, object]) -> dict[str, float]:
    lines = order.get("lines", []) or []
    line_count = len(lines) if isinstance(lines, (list, tuple)) else 0
    total = max(0.0, as_float(order.get("total_amount")))
    discount = max(0.0, as_float(order.get("discount_amount")))
    shipping = max(0.0, as_float(order.get("shipping_amount")))
    item_quantity = 0.0
    if isinstance(lines, (list, tuple)):
        item_quantity = sum(max(0.0, as_float(line.get("quantity", 1))) for line in lines if isinstance(line, dict))
    return {
        "total": total,
        "lines": float(line_count),
        "item_quantity": item_quantity,
        "average_line_value": safe_ratio(total, line_count),
        "discount_ratio": bounded(safe_ratio(discount, total)),
        "shipping_ratio": bounded(safe_ratio(shipping, total)),
        "customer_known": float(bool(order.get("customer_id"))),
        "billing_shipping_match": float(bool(order.get("billing_shipping_match", True))),
        "age_hours": age_hours(order.get("created_at")),
        "high_value": float(total >= max(250.0, as_float(order.get("high_value_threshold", 250.0)))),
    }
