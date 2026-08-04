from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class OrderValidationResult:
    valid: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    line_count: int
    quantity: int
    total: Decimal

    def as_dict(self) -> dict[str, object]:
        result = asdict(self); result["total"] = str(self.total); return result


def validate_paid_order(order: dict[str, object]) -> list[str]:
    return list(validate_order(order).errors)


def validate_order(order: dict[str, object]) -> OrderValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    status = str(order.get("financial_status", "")).lower()
    if status not in {"paid", "partially_refunded"}:
        errors.append("Paiement non confirmé.")
    if not order.get("shipping_address"):
        errors.append("Adresse de livraison absente.")
    lines = order.get("lines") or []
    if not isinstance(lines, list) or not lines:
        errors.append("Commande sans article."); lines = []
    quantity = 0
    for index, line in enumerate(lines):
        if not isinstance(line, dict):
            errors.append(f"Ligne {index} invalide."); continue
        qty = int(line.get("quantity", 0) or 0)
        quantity += max(0, qty)
        if qty <= 0: errors.append(f"Quantité invalide à la ligne {index}.")
        if not line.get("sku"): warnings.append(f"SKU absent à la ligne {index}.")
    total = Decimal(str(order.get("total_amount", order.get("total", 0)) or 0))
    if total < 0: errors.append("Total de commande négatif.")
    return OrderValidationResult(not errors, tuple(errors), tuple(warnings), len(lines), quantity, total)
