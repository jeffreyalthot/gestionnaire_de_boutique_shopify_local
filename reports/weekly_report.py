from __future__ import annotations

from typing import Any

from reports.report_base import TimeWindowReport, aggregate, ratio, grouped_summary


class WeeklyReport(TimeWindowReport):
    name = 'weekly_orders'
    query = 'SELECT * FROM orders WHERE {time_filter} ORDER BY created_at DESC'
    default_days = 7

    def summarize(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        return {"orders": len(rows), "revenue_cad": aggregate(rows,"revenue_cad"), "profit_cad": aggregate(rows,"profit_cad")}
