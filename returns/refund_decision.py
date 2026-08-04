from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True, slots=True)
class RefundDecision:
    approved: bool
    amount_cad: float
    reason: str
    approval_required: bool = False
    refundable_balance_cad: float = 0.0
    restock: bool = False
    customer_message_key: str = ""
    risk_flags: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, object]:
        return asdict(self)

    @classmethod
    def build(
        cls,
        approved: bool,
        amount: object,
        reason: str,
        *,
        approval_required: bool = False,
        refundable_balance: object = 0,
        restock: bool = False,
        customer_message_key: str = "",
        risk_flags: tuple[str, ...] = (),
    ) -> "RefundDecision":
        money = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        balance = Decimal(str(refundable_balance)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return cls(approved, float(money), reason, approval_required, float(balance), restock, customer_message_key, risk_flags)
