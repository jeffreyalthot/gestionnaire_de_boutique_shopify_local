from __future__ import annotations

from typing import Any

from reports.report_base import QueryReport, aggregate, ratio, grouped_summary


class RefundReport(QueryReport):
    name = 'refunds'
    query = "SELECT id,name,total_amount,financial_status,profit_cad,updated_at FROM orders WHERE financial_status LIKE '%refund%' ORDER BY updated_at DESC"

    def summarize(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        return {"orders": len(rows), "exposure_cad": aggregate(rows,"total_amount"), "negative_profit_cad": aggregate((r for r in rows if float(r.get("profit_cad",0) or 0)<0),"profit_cad")}
