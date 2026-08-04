from __future__ import annotations

from ai.features.base import as_float, bounded, safe_ratio


def pricing_features(item: dict[str, object]) -> dict[str, float]:
    current = max(0.0, as_float(item.get("current_price")))
    cost = max(0.0, as_float(item.get("landed_cost")))
    competitor = max(0.0, as_float(item.get("competitor_price")))
    return {
        "current_price": current,
        "landed_cost": cost,
        "gross_margin": bounded(safe_ratio(current - cost, current), -1.0, 1.0),
        "competitor_ratio": safe_ratio(current, competitor, 1.0),
        "conversion_rate": bounded(item.get("conversion_rate")),
        "inventory_pressure": bounded(item.get("inventory_pressure")),
        "return_rate": bounded(item.get("return_rate")),
        "price_change_7d": as_float(item.get("price_change_7d")),
    }
