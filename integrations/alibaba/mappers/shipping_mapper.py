from __future__ import annotations

from decimal import Decimal


def map_shipping_quote(data: dict[str, object]) -> dict[str, object]:
    minimum = int(data.get("minDays") or data.get("estimatedDays") or data.get("deliveryDays") or 0)
    maximum = int(data.get("maxDays") or minimum or 0)
    return {
        "amount": Decimal(str(data.get("freight") or data.get("shippingCost") or data.get("amount") or 0)),
        "currency": str(data.get("currency") or "USD"),
        "service": str(data.get("service") or data.get("channelName") or ""),
        "carrier": str(data.get("carrier") or data.get("logisticsCompany") or ""),
        "estimated_days": maximum or minimum,
        "minimum_days": minimum,
        "maximum_days": maximum,
        "tracking": bool(data.get("tracking", data.get("isTraceable", True))),
        "raw": data,
    }
