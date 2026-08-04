from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass(frozen=True, slots=True)
class LifecycleDecision:
    state: str
    action: str
    reason: str


class ProductLifecycle:
    def decide(self, product: dict[str, object], *, now: datetime | None = None) -> LifecycleDecision:
        now = now or datetime.now(timezone.utc)
        status = str(product.get("status", "draft"))
        stock = int(product.get("stock", 0) or 0)
        score = float(product.get("score", 0) or 0)
        updated = product.get("updated_at")
        if isinstance(updated, str):
            try: updated = datetime.fromisoformat(updated)
            except ValueError: updated = now
        if not isinstance(updated, datetime): updated = now
        if status == "quarantined": return LifecycleDecision(status, "hold", "compliance_quarantine")
        if stock <= 0: return LifecycleDecision("paused", "unpublish", "out_of_stock")
        if score < .45: return LifecycleDecision("review", "manual_review", "low_quality_score")
        if now - updated > timedelta(days=90): return LifecycleDecision("stale", "refresh", "stale_product_data")
        return LifecycleDecision(status, "keep", "healthy")
