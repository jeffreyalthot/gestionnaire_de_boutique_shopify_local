from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class CompensationStep:
    action: str
    priority: int
    required: bool
    reason: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class PurchaseCompensator:
    def build_plan(
        self,
        *,
        intent_status: str,
        supplier_supports_cancel: bool,
        payment_captured: bool,
        inventory_reserved: bool = True,
        customer_notified: bool = False,
    ) -> tuple[CompensationStep, ...]:
        status = str(intent_status).lower()
        steps: list[CompensationStep] = []
        if supplier_supports_cancel and status not in {"cancelled", "delivered", "refunded", "closed"}:
            steps.append(CompensationStep("cancel_supplier_order", 10, True, "supplier_order_reversible"))
        if payment_captured:
            steps.append(CompensationStep("request_supplier_refund", 20, True, "funds_captured"))
        if inventory_reserved:
            steps.append(CompensationStep("release_inventory_reservation", 30, True, "reservation_no_longer_needed"))
        steps.append(CompensationStep("hold_customer_order", 40, True, "prevent_invalid_fulfillment"))
        if not customer_notified:
            steps.append(CompensationStep("notify_customer_delay", 50, False, "customer_expectation_management"))
        steps.append(CompensationStep("open_exception", 60, True, "operator_visibility"))
        return tuple(sorted(steps, key=lambda step: step.priority))

    def plan(self, *, intent_status: str, supplier_supports_cancel: bool, payment_captured: bool) -> tuple[str, ...]:
        return tuple(step.action for step in self.build_plan(
            intent_status=intent_status,
            supplier_supports_cancel=supplier_supports_cancel,
            payment_captured=payment_captured,
        ) if step.action != "notify_customer_delay")
