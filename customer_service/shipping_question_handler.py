from __future__ import annotations

from customer_service.service_result import ServiceResult


class ShippingQuestionHandler:
    def handle(self, shipments: list[dict[str, object]]) -> ServiceResult:
        if not shipments:
            return ServiceResult("shipping_question", "pending", internal_reason="tracking_not_available")
        latest = shipments[0]
        status = str(latest.get("status", "unknown"))
        if status in {"lost", "exception", "undeliverable"}:
            return ServiceResult("shipping_question", "escalate", internal_reason=f"shipping_{status}", approval_required=True, metadata=latest)
        return ServiceResult("shipping_question", "answer", internal_reason="tracking_available", metadata=latest)
