from __future__ import annotations

from typing import Any

from reports.report_base import QueryReport, aggregate, ratio, grouped_summary


class ProfitReport(QueryReport):
    name = 'profit'
    query = 'SELECT id,name,revenue_cad,supplier_cost_cad,shipping_cost_cad,fees_cad,profit_cad,created_at FROM orders ORDER BY created_at DESC'

    def summarize(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        return {"orders": len(rows), "revenue_cad": aggregate(rows,"revenue_cad"), "profit_cad": aggregate(rows,"profit_cad"), "margin": ratio(aggregate(rows,"profit_cad"),aggregate(rows,"revenue_cad"))}
