from __future__ import annotations

from decimal import Decimal

from returns.refund_decision import RefundDecision


class RefundPolicy:
    def __init__(self, *, return_window_days: int = 30, auto_approval_limit_cad: object = 200, maximum_refund_ratio: object = 1) -> None:
        self.return_window_days = max(0, int(return_window_days))
        self.auto_approval_limit = Decimal(str(auto_approval_limit_cad))
        self.maximum_refund_ratio = min(Decimal("1"), max(Decimal("0"), Decimal(str(maximum_refund_ratio))))

    def decide(
        self,
        *,
        paid_cad: float,
        requested_cad: float,
        reason: str,
        delivered: bool,
        days_since_delivery: int,
        refunded_cad: float = 0,
        return_received: bool = False,
        item_condition: str = "unknown",
        customer_chargebacks: int = 0,
    ) -> RefundDecision:
        paid = max(Decimal("0"), Decimal(str(paid_cad)))
        refunded = max(Decimal("0"), Decimal(str(refunded_cad)))
        requested = max(Decimal("0"), Decimal(str(requested_cad)))
        refundable = max(Decimal("0"), paid - refunded)
        amount = min(refundable, requested, paid * self.maximum_refund_ratio)
        reason_key = str(reason).strip().lower()
        flags: list[str] = []
        if amount <= 0:
            return RefundDecision.build(False, 0, "invalid_amount", refundable_balance=refundable)
        if delivered and int(days_since_delivery) > self.return_window_days and reason_key not in {"warranty", "unsafe", "recall"}:
            return RefundDecision.build(False, 0, "window_expired", refundable_balance=refundable)
        if customer_chargebacks > 0:
            flags.append("prior_chargeback")
        if reason_key in {"fraud", "chargeback"}:
            flags.append("financial_dispute")
        if delivered and reason_key in {"changed_mind", "wrong_size", "not_needed"} and not return_received:
            return RefundDecision.build(False, 0, "return_required", refundable_balance=refundable, customer_message_key="return_required")
        damaged = item_condition.lower() in {"damaged", "used", "incomplete"}
        restock = return_received and not damaged
        approval = amount >= self.auto_approval_limit or bool(flags) or reason_key in {"warranty", "unsafe", "recall"}
        return RefundDecision.build(
            True,
            amount,
            "eligible",
            approval_required=approval,
            refundable_balance=refundable - amount,
            restock=restock,
            customer_message_key="refund_approved" if not approval else "refund_pending_approval",
            risk_flags=tuple(flags),
        )
