from __future__ import annotations

from customer_service.service_result import ServiceResult
from returns.return_eligibility import ReturnEligibility


class ReturnRequestHandler:
    def __init__(self, eligibility: ReturnEligibility | None = None) -> None:
        self.eligibility = eligibility or ReturnEligibility()

    def handle(self, *, delivered_days_ago: int, category: str = "general", final_sale: bool = False,
               opened: bool = False) -> ServiceResult:
        result = self.eligibility.evaluate(delivered_days_ago=delivered_days_ago, category=category,
                                           final_sale=final_sale, opened=opened)
        return ServiceResult("return", "eligible" if result["eligible"] else "rejected",
                             internal_reason=str(result["reason"]), metadata=result)
