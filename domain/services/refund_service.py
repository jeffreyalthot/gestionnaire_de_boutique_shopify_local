from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True, slots=True)
class RefundDecision:
    refundable: Decimal
    requested: Decimal
    approved: Decimal
    status: str

    def as_dict(self) -> dict[str, str]:
        return {key: str(value) for key, value in asdict(self).items()}


def refundable_amount(paid: Decimal, already_refunded: Decimal) -> Decimal:
    return max(Decimal("0"), Decimal(str(paid)) - Decimal(str(already_refunded)))


def evaluate_refund(paid: Decimal, already_refunded: Decimal, requested: Decimal) -> RefundDecision:
    available = refundable_amount(paid, already_refunded)
    requested_value = max(Decimal("0"), Decimal(str(requested)))
    approved = min(available, requested_value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    status = "approved" if approved == requested_value else ("partial" if approved > 0 else "rejected")
    return RefundDecision(available, requested_value, approved, status)
