from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from decimal import Decimal
from typing import Iterable


@dataclass(frozen=True, slots=True)
class ReturnAnalyticsSummary:
    returns: int
    orders: int
    return_rate: float
    refund_amount_cad: float
    average_refund_cad: float
    reasons: dict[str, int]
    products: dict[str, int]
    suppliers: dict[str, int]
    preventable_rate: float
    recommendations: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class ReturnAnalytics:
    PREVENTABLE = {"wrong_item", "damaged", "not_as_described", "quality", "late_delivery"}

    def detailed(self, returns: Iterable[dict[str, object]], orders: int) -> ReturnAnalyticsSummary:
        rows = [dict(row) for row in returns]
        reasons = Counter(str(row.get("reason") or "unknown") for row in rows)
        products = Counter(str(row.get("product_id") or row.get("sku") or "unknown") for row in rows)
        suppliers = Counter(str(row.get("supplier_id") or "unknown") for row in rows)
        refunds = sum((Decimal(str(row.get("refund_amount_cad") or 0)) for row in rows), Decimal("0"))
        preventable = sum(count for reason, count in reasons.items() if reason in self.PREVENTABLE)
        recommendations: list[str] = []
        if rows and preventable / len(rows) >= 0.3:
            recommendations.append("audit_supplier_and_product_quality")
        if reasons.get("late_delivery", 0):
            recommendations.append("review_shipping_routes")
        if reasons.get("not_as_described", 0):
            recommendations.append("improve_product_content")
        return ReturnAnalyticsSummary(
            returns=len(rows),
            orders=max(0, int(orders)),
            return_rate=round(len(rows) / max(1, int(orders)), 4),
            refund_amount_cad=round(float(refunds), 2),
            average_refund_cad=round(float(refunds / max(1, len(rows))), 2),
            reasons=dict(reasons),
            products=dict(products),
            suppliers=dict(suppliers),
            preventable_rate=round(preventable / max(1, len(rows)), 4),
            recommendations=tuple(dict.fromkeys(recommendations)),
        )

    def summarize(self, returns: list[dict[str, object]], orders: int) -> dict[str, object]:
        summary = self.detailed(returns, orders)
        return {"returns": summary.returns, "return_rate": summary.return_rate, "reasons": summary.reasons}
