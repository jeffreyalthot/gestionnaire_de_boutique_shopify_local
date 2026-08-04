from __future__ import annotations

from customer_service.service_result import ServiceResult


class CancellationRequestHandler:
    def handle(self, context: dict[str, object]) -> ServiceResult:
        order = dict(context.get("order") or {})
        financial = str(order.get("financial_status", ""))
        fulfillment = str(order.get("fulfillment_status", ""))
        procurement = str(order.get("procurement_status", ""))
        if fulfillment in {"fulfilled", "partial"} or procurement in {"submitted", "paid", "shipped"}:
            return ServiceResult("cancellation", "escalate", internal_reason="order_already_in_fulfillment", approval_required=True)
        if financial not in {"paid", "authorized", "pending"}:
            return ServiceResult("cancellation", "rejected", internal_reason="order_not_cancellable")
        return ServiceResult("cancellation", "eligible", internal_reason="pre_fulfillment", approval_required=financial in {"paid", "authorized"})
