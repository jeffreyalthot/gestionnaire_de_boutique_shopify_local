from __future__ import annotations

from typing import Any


ALLOWED_DIMENSIONS = {
    "store", "channel", "market", "country", "currency", "product", "variant",
    "supplier", "campaign", "order_status", "fulfillment_status", "risk", "workflow",
}


def normalize_dimensions(dimensions: dict[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    for key, value in dimensions.items():
        normalized = str(key).strip().lower()
        if normalized not in ALLOWED_DIMENSIONS:
            continue
        text = str(value).strip()
        if text:
            result[normalized] = text[:200]
    return result
