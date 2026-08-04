from __future__ import annotations


class RetentionSegment:
    def classify(self, days_since_last_order: int, order_count: int) -> tuple[str, float]:
        days = max(0, days_since_last_order)
        if order_count <= 0:
            return "prospect", 0.2
        if days <= 30:
            return "active", 1.0
        if days <= 90:
            return "cooling", 0.7
        if days <= 180:
            return "at_risk", 0.4
        return "lapsed", 0.1
