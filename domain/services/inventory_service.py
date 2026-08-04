from __future__ import annotations

from dataclasses import asdict, dataclass
from math import ceil


@dataclass(frozen=True, slots=True)
class InventoryDecision:
    sellable: int
    reorder_point: int
    reorder_quantity: int
    status: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def sellable_stock(supplier_stock: int, safety_stock: int, reserved: int = 0) -> int:
    return max(0, int(supplier_stock) - max(0, int(safety_stock)) - max(0, int(reserved)))


class InventoryService:
    def evaluate(
        self,
        *,
        supplier_stock: int,
        safety_stock: int,
        reserved: int = 0,
        average_daily_demand: float = 0.0,
        lead_time_days: float = 0.0,
        target_coverage_days: float = 30.0,
    ) -> InventoryDecision:
        sellable = sellable_stock(supplier_stock, safety_stock, reserved)
        reorder_point = max(
            max(0, int(safety_stock)),
            ceil(max(0.0, average_daily_demand) * max(0.0, lead_time_days)) + max(0, int(safety_stock)),
        )
        target = ceil(max(0.0, average_daily_demand) * max(0.0, target_coverage_days))
        reorder_quantity = max(0, target - sellable)
        status = "out_of_stock" if sellable == 0 else ("reorder" if sellable <= reorder_point else "healthy")
        return InventoryDecision(sellable, reorder_point, reorder_quantity, status)
