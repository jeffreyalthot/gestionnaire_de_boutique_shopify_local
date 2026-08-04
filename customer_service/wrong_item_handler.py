from __future__ import annotations

from customer_service.service_result import ServiceResult


class WrongItemHandler:
    def handle(self, *, ordered_sku: str, received_sku: str, evidence_count: int = 0) -> ServiceResult:
        if ordered_sku == received_sku:
            return ServiceResult("wrong_item", "rejected", internal_reason="sku_matches")
        if evidence_count <= 0:
            return ServiceResult("wrong_item", "request_evidence", internal_reason="photo_required")
        return ServiceResult("wrong_item", "eligible", internal_reason="sku_mismatch", approval_required=True,
                             metadata={"ordered_sku": ordered_sku, "received_sku": received_sku})
