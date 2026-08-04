from __future__ import annotations

from customer_service.service_result import ServiceResult


class DamagedItemHandler:
    def handle(self, *, delivered: bool, evidence_count: int, order_amount_cad: float) -> ServiceResult:
        if not delivered:
            return ServiceResult("damaged_item", "hold", internal_reason="delivery_not_confirmed")
        if evidence_count <= 0:
            return ServiceResult("damaged_item", "request_evidence", internal_reason="evidence_required")
        return ServiceResult("damaged_item", "eligible", internal_reason="damage_evidence_received",
                             approval_required=order_amount_cad >= 100, metadata={"recommended": "replace_or_refund"})
