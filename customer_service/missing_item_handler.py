from __future__ import annotations

from customer_service.service_result import ServiceResult


class MissingItemHandler:
    def handle(self, *, expected_quantity: int, delivered_quantity: int, package_delivered: bool) -> ServiceResult:
        missing = max(0, expected_quantity - delivered_quantity)
        if not package_delivered:
            return ServiceResult("missing_item", "route_shipping", internal_reason="package_not_delivered")
        if missing <= 0:
            return ServiceResult("missing_item", "rejected", internal_reason="quantity_complete")
        return ServiceResult("missing_item", "eligible", internal_reason="partial_delivery", metadata={"missing_quantity": missing})
