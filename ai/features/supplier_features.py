from __future__ import annotations

from ai.features.base import as_float, bounded, safe_ratio


def supplier_features(supplier: dict[str, object]) -> dict[str, float]:
    orders = max(0.0, as_float(supplier.get("orders_count")))
    defects = max(0.0, as_float(supplier.get("defect_count")))
    disputes = max(0.0, as_float(supplier.get("dispute_count")))
    return {
        "orders": orders,
        "years_active": max(0.0, as_float(supplier.get("years_active"))),
        "response_rate": bounded(supplier.get("response_rate")),
        "on_time_rate": bounded(supplier.get("on_time_rate")),
        "defect_rate": bounded(supplier.get("defect_rate", safe_ratio(defects, orders))),
        "dispute_rate": bounded(safe_ratio(disputes, orders)),
        "trade_assurance": float(bool(supplier.get("trade_assurance"))),
        "verified": float(bool(supplier.get("verified"))),
        "minimum_order_value": max(0.0, as_float(supplier.get("minimum_order_value"))),
        "score": bounded(supplier.get("score")),
    }
