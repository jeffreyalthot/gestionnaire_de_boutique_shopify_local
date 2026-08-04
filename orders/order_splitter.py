from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class SupplierOrderGroup:
    supplier_id: str
    lines: tuple[dict[str, object], ...]
    units: int
    estimated_cost: Decimal

    def as_dict(self) -> dict[str, object]:
        value = asdict(self); value["estimated_cost"] = str(self.estimated_cost); return value


class OrderSplitter:
    def by_supplier(self, lines: list[dict[str, object]]) -> dict[str, list[dict[str, object]]]:
        return {group.supplier_id: [dict(item) for item in group.lines] for group in self.groups(lines)}

    def groups(self, lines: list[dict[str, object]]) -> tuple[SupplierOrderGroup, ...]:
        grouped: dict[str, list[dict[str, object]]] = {}
        for line in lines:
            supplier = str(line.get("supplier_id", "")).strip()
            if not supplier:
                raise ValueError("supplier_id manquant")
            quantity = int(line.get("quantity", 1) or 1)
            if quantity <= 0:
                raise ValueError("quantity invalide")
            normalized = dict(line)
            normalized.setdefault("quantity", quantity)
            grouped.setdefault(supplier, []).append(normalized)
        result = []
        for supplier, items in sorted(grouped.items()):
            units = sum(int(item.get("quantity", 1) or 1) for item in items)
            cost = sum((Decimal(str(item.get("unit_supplier_cost_cad", item.get("cost", 0)) or 0)) * int(item.get("quantity", 1) or 1) for item in items), Decimal("0"))
            result.append(SupplierOrderGroup(supplier, tuple(items), units, cost))
        return tuple(result)
