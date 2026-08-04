from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal
from typing import Iterable

from finance.payout_reconciler import reconcile_payout


@dataclass(frozen=True, slots=True)
class SupplierPaymentMatch:
    reference: str
    expected: Decimal
    received: Decimal
    variance: Decimal
    status: str

    def as_dict(self) -> dict[str, object]:
        return {key: str(value) if isinstance(value, Decimal) else value for key, value in asdict(self).items()}


class SupplierPaymentReconciler:
    def __init__(self, tolerance: Decimal = Decimal("0.01")) -> None:
        self.tolerance = abs(Decimal(str(tolerance)))

    def match(self, reference: str, expected: Decimal, received: Decimal) -> SupplierPaymentMatch:
        expected_value = Decimal(str(expected))
        received_value = Decimal(str(received))
        variance = received_value - expected_value
        status = "balanced" if abs(variance) <= self.tolerance else ("overpaid" if variance > 0 else "underpaid")
        return SupplierPaymentMatch(str(reference), expected_value, received_value, variance, status)

    def reconcile_many(self, items: Iterable[dict[str, object]]) -> tuple[SupplierPaymentMatch, ...]:
        return tuple(self.match(str(item.get("reference", "")), Decimal(str(item.get("expected", 0))), Decimal(str(item.get("received", 0)))) for item in items)


def reconcile_supplier_payment(expected: float, received: float, tolerance: float = 0.01) -> dict[str, object]:
    return reconcile_payout(expected, received, tolerance)
