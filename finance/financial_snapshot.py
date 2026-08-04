from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from decimal import Decimal

from infrastructure.database.engine import Database


@dataclass(frozen=True, slots=True)
class FinancialSnapshot:
    revenue: Decimal
    supplier_cost: Decimal
    shipping_cost: Decimal
    fees: Decimal
    refunds: Decimal
    profit: Decimal
    margin_percent: Decimal
    counts: dict[str, int]
    generated_at: str

    def as_dict(self) -> dict[str, object]:
        result = asdict(self)
        for key in ("revenue", "supplier_cost", "shipping_cost", "fees", "refunds", "profit", "margin_percent"):
            result[key] = str(result[key])
        return result


class FinancialSnapshotBuilder:
    def build(self, db: Database) -> FinancialSnapshot:
        raw = db.financial_snapshot()
        revenue = Decimal(str(raw.get("revenue", 0) or 0))
        supplier = Decimal(str(raw.get("supplier_cost", raw.get("supplier", 0)) or 0))
        shipping = Decimal(str(raw.get("shipping_cost", raw.get("shipping", 0)) or 0))
        fees = Decimal(str(raw.get("fees", 0) or 0))
        refunds = Decimal(str(raw.get("refunds", 0) or 0))
        profit = Decimal(str(raw.get("profit", revenue - supplier - shipping - fees - refunds) or 0))
        margin = profit / revenue * Decimal("100") if revenue else Decimal("0")
        counts = {str(key): int(value) for key, value in db.counts().items()}
        return FinancialSnapshot(revenue, supplier, shipping, fees, refunds, profit, margin, counts, datetime.now(timezone.utc).isoformat())


def snapshot(db: Database) -> dict[str, object]:
    built = FinancialSnapshotBuilder().build(db)
    return {"finance": db.financial_snapshot(), "counts": db.counts(), "normalized": built.as_dict()}
