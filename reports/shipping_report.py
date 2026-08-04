from __future__ import annotations

from typing import Any

from reports.report_base import QueryReport, aggregate, ratio, grouped_summary


class ShippingReport(QueryReport):
    name = 'shipping'
    query = 'SELECT * FROM shipments ORDER BY updated_at DESC'

    def summarize(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        return {"shipments": len(rows), "by_status": grouped_summary(rows,"status"), "with_tracking": sum(bool(r.get("tracking_number")) for r in rows)}
