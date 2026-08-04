from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class ReturnLabelPlan:
    strategy: str
    payer: str
    estimated_cost_cad: float
    return_required: bool
    approval_required: bool
    reason: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class ReturnLabelPlanner:
    MERCHANT_FAULT = {"damaged", "wrong_item", "not_as_described", "defective"}

    def detailed_plan(
        self,
        *,
        reason: str,
        item_value_cad: float,
        return_shipping_cad: float,
        hazardous: bool = False,
        oversized: bool = False,
        international: bool = False,
    ) -> ReturnLabelPlan:
        value = max(0.0, float(item_value_cad))
        shipping = max(0.0, float(return_shipping_cad))
        normalized_reason = str(reason).strip().lower()
        if hazardous:
            return ReturnLabelPlan("manual_hazardous_review", "merchant", shipping, True, True, "hazardous_goods")
        if shipping >= value * 0.6 or (international and shipping >= value * 0.4):
            return ReturnLabelPlan("refund_without_return_review", "merchant", 0.0, False, True, "uneconomical_return")
        if normalized_reason in self.MERCHANT_FAULT:
            strategy = "merchant_paid_label"
            payer = "merchant"
        else:
            strategy = "customer_paid_label"
            payer = "customer"
        if oversized:
            strategy = "carrier_pickup_review"
        return ReturnLabelPlan(strategy, payer, round(shipping, 2), True, oversized, "policy_match")

    def plan(self, *, reason: str, item_value_cad: float, return_shipping_cad: float) -> str:
        return self.detailed_plan(reason=reason, item_value_cad=item_value_cad, return_shipping_cad=return_shipping_cad).strategy
