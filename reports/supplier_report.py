from __future__ import annotations

from typing import Any

from reports.report_base import QueryReport, aggregate, ratio, grouped_summary


class SupplierReport(QueryReport):
    name = 'suppliers'
    query = 'SELECT supplier_id,COUNT(*) products,ROUND(AVG(score),4) score,ROUND(AVG(landed_cost_cad),2) average_landed_cost_cad FROM products GROUP BY supplier_id ORDER BY score DESC'

    def summarize(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        return {"suppliers": len(rows), "products": sum(int(r.get("products",0) or 0) for r in rows), "average_score": round(sum(float(r.get("score",0) or 0) for r in rows)/len(rows),4) if rows else 0.0}
