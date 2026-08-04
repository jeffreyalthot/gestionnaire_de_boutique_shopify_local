from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class RestockingDecision:
    received: int
    restockable: int
    damaged: int
    missing: int
    quarantine: int
    condition: str
    inventory_value_cad: Decimal

    def as_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["inventory_value_cad"] = str(self.inventory_value_cad)
        return result


class RestockingService:
    def quantity(self, *, received: int, damaged: int, missing: int) -> int:
        return self.assess(received=received, damaged=damaged, missing=missing).restockable

    def assess(
        self,
        *,
        received: int,
        damaged: int = 0,
        missing: int = 0,
        opened: int = 0,
        unsafe: int = 0,
        unit_cost_cad: object = 0,
    ) -> RestockingDecision:
        values = [int(received), int(damaged), int(missing), int(opened), int(unsafe)]
        if any(value < 0 for value in values):
            raise ValueError("quantité de retour invalide")
        damaged_total = min(values[0], values[1] + values[3])
        missing_total = min(max(0, values[0] - damaged_total), values[2])
        quarantine = min(max(0, values[0] - damaged_total - missing_total), values[4])
        restockable = max(0, values[0] - damaged_total - missing_total - quarantine)
        condition = "sellable" if restockable == values[0] else "mixed" if restockable else "unsellable"
        value = Decimal(str(unit_cost_cad)) * restockable
        return RestockingDecision(values[0], restockable, damaged_total, missing_total, quarantine, condition, value)
