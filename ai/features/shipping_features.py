from __future__ import annotations

from ai.features.base import as_float, bounded, safe_ratio


def shipping_features(shipment: dict[str, object]) -> dict[str, float]:
    quoted = max(0.0, as_float(shipment.get("quoted_days")))
    actual = max(0.0, as_float(shipment.get("actual_days")))
    quoted_cost = max(0.0, as_float(shipment.get("quoted_cost")))
    actual_cost = max(0.0, as_float(shipment.get("actual_cost")))
    return {
        "quoted_days": quoted,
        "actual_days": actual,
        "delay_days": max(0.0, actual - quoted),
        "on_time": float(actual > 0 and actual <= quoted),
        "cost_variance_ratio": safe_ratio(actual_cost - quoted_cost, quoted_cost),
        "tracking_event_count": max(0.0, as_float(shipment.get("tracking_event_count"))),
        "carrier_score": bounded(shipment.get("carrier_score")),
        "destination_risk": bounded(shipment.get("destination_risk")),
    }
