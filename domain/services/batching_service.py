from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal
from typing import Iterable


@dataclass(frozen=True, slots=True)
class BatchDecision:
    ready: bool
    total_cad: Decimal
    order_count: int
    supplier_count: int
    reason: str

    def as_dict(self) -> dict[str, object]:
        value = asdict(self)
        value["total_cad"] = str(self.total_cad)
        return value


def threshold_reached(total_cad: float, threshold_cad: float) -> bool:
    return Decimal(str(total_cad)) >= Decimal(str(threshold_cad))


class BatchingService:
    def __init__(self, *, threshold_cad: Decimal = Decimal("100"), maximum_orders: int = 100) -> None:
        self.threshold_cad = Decimal(str(threshold_cad))
        self.maximum_orders = max(1, int(maximum_orders))

    def evaluate(self, orders: Iterable[dict[str, object]]) -> BatchDecision:
        items = list(orders)
        total = sum((Decimal(str(item.get("amount_cad", 0) or 0)) for item in items), Decimal("0"))
        suppliers = {str(item.get("supplier_id", "")) for item in items if item.get("supplier_id")}
        if not items:
            return BatchDecision(False, total, 0, 0, "empty")
        if len(items) >= self.maximum_orders:
            return BatchDecision(True, total, len(items), len(suppliers), "maximum_orders")
        if total >= self.threshold_cad:
            return BatchDecision(True, total, len(items), len(suppliers), "value_threshold")
        return BatchDecision(False, total, len(items), len(suppliers), "threshold_not_reached")

    def group_by_supplier(self, orders: Iterable[dict[str, object]]) -> dict[str, list[dict[str, object]]]:
        groups: dict[str, list[dict[str, object]]] = {}
        for item in orders:
            supplier = str(item.get("supplier_id", "unmapped")) or "unmapped"
            groups.setdefault(supplier, []).append(dict(item))
        return groups
