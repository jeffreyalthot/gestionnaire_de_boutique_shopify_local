from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from customers.segments.retention_segment import RetentionSegment
from customers.segments.risk_segment import RiskSegment
from customers.segments.value_segment import ValueSegment


class SegmentBuilder:
    def __init__(self, db: Any) -> None:
        self.db = db
        self.value = ValueSegment()
        self.risk = RiskSegment()
        self.retention = RetentionSegment()

    def build(self, customer_id: str, *, lifetime_value_cad: float, order_count: int,
              risk_score: float, days_since_last_order: int) -> tuple[dict[str, object], ...]:
        segments = (
            ("value", *self.value.classify(lifetime_value_cad, order_count)),
            ("risk", *self.risk.classify(risk_score)),
            ("retention", *self.retention.classify(days_since_last_order, order_count)),
        )
        now = datetime.now(timezone.utc).isoformat()
        result: list[dict[str, object]] = []
        for family, name, score in segments:
            segment = f"{family}:{name}"
            self.db.execute(
                "INSERT INTO customer_segment_memberships(customer_id,segment,score,reason,updated_at) VALUES(?,?,?,?,?) "
                "ON CONFLICT(customer_id,segment) DO UPDATE SET score=excluded.score,reason=excluded.reason,updated_at=excluded.updated_at",
                (customer_id, segment, float(score), "deterministic_segmentation", now),
            )
            result.append({"segment": segment, "score": float(score)})
        return tuple(result)
