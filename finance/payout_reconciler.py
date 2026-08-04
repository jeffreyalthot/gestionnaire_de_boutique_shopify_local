from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP


def reconcile_payout(expected: float, received: float, tolerance: float = 0.01) -> dict[str, object]:
    expected_value = Decimal(str(expected))
    received_value = Decimal(str(received))
    variance = received_value - expected_value
    tolerance_value = abs(Decimal(str(tolerance)))
    return {
        "balanced": abs(variance) <= tolerance_value,
        "variance": float(variance),
        "variance_decimal": str(variance.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
        "status": "balanced" if abs(variance) <= tolerance_value else ("over" if variance > 0 else "under"),
    }
