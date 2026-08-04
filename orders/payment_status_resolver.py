from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class PaymentResolution:
    status: str
    total: Decimal
    paid: Decimal
    refunded: Decimal
    outstanding: Decimal

    def as_dict(self) -> dict[str, object]:
        return {key: str(value) if isinstance(value, Decimal) else value for key, value in asdict(self).items()}


class PaymentStatusResolver:
    def resolve(self, *, total: float, paid: float, refunded: float = 0.0, voided: bool = False) -> str:
        return self.details(total=total, paid=paid, refunded=refunded, voided=voided).status

    def details(self, *, total: float, paid: float, refunded: float = 0.0, voided: bool = False) -> PaymentResolution:
        total_value = max(Decimal("0"), Decimal(str(total)))
        paid_value = max(Decimal("0"), Decimal(str(paid)))
        refund_value = max(Decimal("0"), min(paid_value, Decimal(str(refunded))))
        if voided: status = "voided"
        elif refund_value >= paid_value > 0: status = "refunded"
        elif refund_value > 0: status = "partially_refunded"
        elif paid_value >= total_value > 0: status = "paid"
        elif paid_value > 0: status = "partially_paid"
        else: status = "pending"
        outstanding = max(Decimal("0"), total_value - paid_value)
        return PaymentResolution(status, total_value, paid_value, refund_value, outstanding)
