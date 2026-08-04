from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True, slots=True)
class ReturnDecision:
    eligible: bool
    reason: str
    manual_review: bool = False


class ReturnEligibility:
    def evaluate(self, *, delivered_at: datetime, requested_at: datetime, category: str, final_sale: bool = False, damaged: bool = False, window_days: int = 30) -> ReturnDecision:
        if damaged:
            return ReturnDecision(True, "damaged_item")
        if final_sale:
            return ReturnDecision(False, "final_sale")
        if category in {"hygiene", "personalized"}:
            return ReturnDecision(False, "non_returnable_category", True)
        if requested_at > delivered_at + timedelta(days=window_days):
            return ReturnDecision(False, "window_expired")
        return ReturnDecision(True, "eligible")
