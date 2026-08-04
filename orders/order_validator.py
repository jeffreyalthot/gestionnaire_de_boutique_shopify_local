from __future__ import annotations

from dataclasses import dataclass

from orders.address_quality import AddressQuality


@dataclass(frozen=True, slots=True)
class OrderValidation:
    valid: bool
    issues: tuple[str, ...]


class OrderValidator:
    def __init__(self) -> None:
        self.address_quality = AddressQuality()

    def validate(self, order: dict[str, object]) -> OrderValidation:
        issues: list[str] = []
        if not str(order.get("id") or order.get("shopify_order_id") or ""):
            issues.append("missing_order_id")
        if float(order.get("total_amount", order.get("total", 0)) or 0) < 0:
            issues.append("negative_total")
        lines = order.get("lines") or []
        if not isinstance(lines, list) or not lines:
            issues.append("missing_lines")
        else:
            for index, line in enumerate(lines):
                if not isinstance(line, dict) or int(line.get("quantity", 0) or 0) <= 0:
                    issues.append(f"invalid_line_{index}")
        address = order.get("shipping_address")
        if isinstance(address, dict):
            issues.extend(self.address_quality.evaluate(address).issues)
        else:
            issues.append("missing_shipping_address")
        return OrderValidation(not issues, tuple(sorted(set(issues))))
