from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class PaymentVerification:
    verified: bool
    status: str
    amount: float
    currency: str
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class PaymentVerificationWorkflow:
    paid_statuses = {"paid", "partially_refunded", "authorized"}

    def inspect(self, order: dict[str, object]) -> PaymentVerification:
        status = str(order.get("financial_status", "")).strip().lower()
        try:
            amount = float(order.get("total_amount", order.get("total_price", 0)) or 0)
        except (TypeError, ValueError):
            amount = 0.0
        currency = str(order.get("currency", "CAD") or "CAD").upper()
        verified = status in self.paid_statuses and amount >= 0 and len(currency) == 3
        reason = "verified" if verified else ("payment_status_not_settled" if status not in self.paid_statuses else "invalid_amount_or_currency")
        return PaymentVerification(verified, status, amount, currency, reason)

    def verify(self, order: dict[str, object]) -> bool:
        return self.inspect(order).verified
