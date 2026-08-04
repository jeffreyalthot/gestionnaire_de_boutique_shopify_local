from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class OrderRoute:
    queue: str
    priority: int
    reason: str
    hold: bool = False

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def route_order(order: dict[str, object]) -> str:
    return OrderRouter().route(order).queue


class OrderRouter:
    def route(self, order: dict[str, object]) -> OrderRoute:
        financial = str(order.get("financial_status", "")).lower()
        risk = str(order.get("risk_level", "unknown")).lower()
        if bool(order.get("cancelled")):
            return OrderRoute("cancelled", 0, "order_cancelled", True)
        if financial not in {"paid", "partially_paid", "partially_refunded"}:
            return OrderRoute("await_payment", 20, "payment_not_confirmed", True)
        if risk in {"high", "critical"}:
            return OrderRoute("manual_risk_review", 5, f"risk_{risk}", True)
        if bool(order.get("mapping_missing")):
            return OrderRoute("mapping_exception", 10, "supplier_mapping_missing", True)
        if bool(order.get("address_invalid")):
            return OrderRoute("address_exception", 10, "shipping_address_invalid", True)
        return OrderRoute("procurement", 50, "ready_for_procurement", False)
