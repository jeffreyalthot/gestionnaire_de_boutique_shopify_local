from __future__ import annotations


class ValueSegment:
    def classify(self, lifetime_value_cad: float, order_count: int) -> tuple[str, float]:
        if lifetime_value_cad >= 2000 or order_count >= 20:
            return "platinum", 1.0
        if lifetime_value_cad >= 1000 or order_count >= 10:
            return "gold", 0.85
        if lifetime_value_cad >= 300 or order_count >= 3:
            return "silver", 0.65
        return "new", 0.35
