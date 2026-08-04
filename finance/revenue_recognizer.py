from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal

from finance.accounting_engine import AccountingEngine


@dataclass(frozen=True, slots=True)
class RevenueRecognition:
    order_id: str
    amount: Decimal
    recognized: bool
    reason: str

    def as_dict(self) -> dict[str, object]:
        value = asdict(self); value["amount"] = str(self.amount); return value


class RevenueRecognizer:
    def __init__(self, engine: AccountingEngine) -> None:
        self.engine = engine
        self._recognized: set[str] = set()

    def recognize(self, order_id: str, amount: Decimal, *, paid: bool = True) -> RevenueRecognition:
        if not order_id:
            raise ValueError("order_id is required")
        value = Decimal(str(amount))
        if value < 0:
            raise ValueError("amount cannot be negative")
        if not paid:
            return RevenueRecognition(order_id, value, False, "payment_not_confirmed")
        if order_id in self._recognized:
            return RevenueRecognition(order_id, value, False, "already_recognized")
        self.engine.recognize_sale(order_id, float(value))
        self._recognized.add(order_id)
        return RevenueRecognition(order_id, value, True, "recognized")


def recognize_paid_order(engine: AccountingEngine, order_id: str, amount: float) -> None:
    engine.recognize_sale(order_id, amount)
