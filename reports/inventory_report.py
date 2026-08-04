from __future__ import annotations

from typing import Any

from reports.report_base import QueryReport, aggregate, ratio, grouped_summary


class InventoryReport(QueryReport):
    name = 'inventory'
    query = 'SELECT id,title,status,stock,sale_price_cad,landed_cost_cad,updated_at FROM products ORDER BY stock ASC,updated_at DESC'

    def summarize(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        return {"products": len(rows), "units": sum(int(r.get("stock",0) or 0) for r in rows), "out_of_stock": sum(int(r.get("stock",0) or 0)<=0 for r in rows), "inventory_value_cad": aggregate(({**r,"value":float(r.get("stock",0) or 0)*float(r.get("landed_cost_cad",0) or 0)} for r in rows),"value")}
