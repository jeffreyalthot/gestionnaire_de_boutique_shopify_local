from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class SupplierOrderAssessment:
    status: str
    action: str
    terminal: bool
    overdue: bool
    severity: str
    next_check_minutes: int
    reason: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class SupplierOrderMonitor:
    TERMINAL = {"cancelled", "delivered", "refunded", "closed"}

    def assess(self, status: str, *, age_hours: float, tracking_available: bool = False) -> SupplierOrderAssessment:
        normalized = str(status).strip().lower() or "unknown"
        age = max(0.0, float(age_hours))
        if normalized in self.TERMINAL:
            return SupplierOrderAssessment(normalized, "none", True, False, "none", 0, "terminal")
        if normalized in {"payment_failed", "creation_failed"}:
            return SupplierOrderAssessment(normalized, "retry_or_escalate", False, True, "high", 15, "supplier_transaction_failed")
        if normalized in {"awaiting_shipment", "paid"} and age >= 120:
            return SupplierOrderAssessment(normalized, "escalate_supplier", False, True, "high", 60, "shipment_severely_overdue")
        if normalized in {"awaiting_shipment", "paid"} and age >= 72:
            return SupplierOrderAssessment(normalized, "contact_supplier", False, True, "medium", 180, "shipment_overdue")
        if normalized == "shipped":
            action = "sync_tracking" if tracking_available else "request_tracking"
            return SupplierOrderAssessment(normalized, action, False, False, "low", 120, "shipment_dispatched")
        if normalized in {"processing", "created", "submitted"} and age >= 24:
            return SupplierOrderAssessment(normalized, "verify_progress", False, True, "medium", 180, "processing_slow")
        return SupplierOrderAssessment(normalized, "monitor", False, False, "none", 360, "within_expected_window")

    def action(self, status: str, *, age_hours: float) -> str:
        return self.assess(status, age_hours=age_hours).action
