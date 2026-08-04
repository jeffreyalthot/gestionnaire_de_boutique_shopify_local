from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class ReturnShippingAssessment:
    status: str
    action: str
    overdue: bool
    severity: str
    next_check_hours: int
    reason: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class ReturnShippingTracker:
    def assess(self, status: str, age_days: int, *, carrier_events: int = 0) -> ReturnShippingAssessment:
        normalized = str(status).strip().lower()
        age = max(0, int(age_days))
        if normalized == "delivered":
            return ReturnShippingAssessment(normalized, "inspect_return", False, "none", 0, "arrived")
        if normalized in {"lost", "exception"}:
            return ReturnShippingAssessment(normalized, "carrier_claim_and_refund_review", True, "high", 4, "carrier_exception")
        if normalized == "in_transit" and age > 21:
            return ReturnShippingAssessment(normalized, "escalate_carrier", True, "high", 12, "severely_overdue")
        if normalized == "in_transit" and age > 14:
            return ReturnShippingAssessment(normalized, "carrier_inquiry", True, "medium", 24, "overdue")
        if normalized == "label_created" and age > 14:
            return ReturnShippingAssessment(normalized, "close_or_reauthorize", True, "medium", 24, "label_unused")
        if normalized == "label_created" and age > 7:
            return ReturnShippingAssessment(normalized, "customer_reminder", True, "low", 48, "awaiting_customer_dropoff")
        if normalized == "in_transit" and carrier_events == 0 and age > 3:
            return ReturnShippingAssessment(normalized, "verify_tracking", True, "low", 24, "missing_scan")
        return ReturnShippingAssessment(normalized or "unknown", "monitor", False, "none", 48, "within_window")

    def action(self, status: str, age_days: int) -> str:
        return self.assess(status, age_days).action
