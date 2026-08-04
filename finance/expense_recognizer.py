from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal

from finance.accounting_engine import AccountingEngine


@dataclass(frozen=True, slots=True)
class ProcurementExpense:
    order_id: str
    product_cost: Decimal
    shipping_cost: Decimal
    total: Decimal

    def as_dict(self) -> dict[str, object]:
        return {key: str(value) if isinstance(value, Decimal) else value for key, value in asdict(self).items()}


def recognize_procurement(engine: AccountingEngine, order_id: str, cost: float, shipping: float) -> None:
    product_cost = Decimal(str(cost)); shipping_cost = Decimal(str(shipping))
    if product_cost < 0 or shipping_cost < 0:
        raise ValueError("procurement costs cannot be negative")
    engine.recognize_supplier_cost(order_id, float(product_cost))
    engine.recognize_shipping(order_id, float(shipping_cost))


def procurement_expense(order_id: str, cost: Decimal, shipping: Decimal) -> ProcurementExpense:
    product = Decimal(str(cost)); freight = Decimal(str(shipping))
    return ProcurementExpense(order_id, product, freight, product + freight)
