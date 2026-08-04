from __future__ import annotations

from dataclasses import asdict, dataclass

from inventory.inventory_availability import InventoryAvailability
from inventory.inventory_position import InventoryPosition


@dataclass(frozen=True, slots=True)
class OversellDecision:
    allowed: bool
    reason: str
    requested: int
    available: int
    supplier_available: int | None

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class OversellPreventer:
    def decide(self, position: InventoryPosition, requested: int) -> tuple[bool, str]:
        value = self.evaluate(position, requested)
        return value.allowed, value.reason

    def evaluate(self, position: InventoryPosition, requested: int) -> OversellDecision:
        requested = int(requested)
        if requested <= 0:
            return OversellDecision(False, "invalid_quantity", requested, position.available, position.supplier_available)
        if not InventoryAvailability().can_fulfill(position, requested):
            return OversellDecision(False, "insufficient_available_inventory", requested, position.available, position.supplier_available)
        return OversellDecision(True, "available", requested, position.available, position.supplier_available)
