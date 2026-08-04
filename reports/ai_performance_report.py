from __future__ import annotations

from typing import Any

from reports.report_base import QueryReport, aggregate, ratio, grouped_summary


class AIPerformanceReport(QueryReport):
    name = 'ai_performance'
    query = 'SELECT decision_type,COUNT(*) decisions,ROUND(AVG(confidence),4) confidence,ROUND(AVG(outcome),4) outcome FROM ai_decisions GROUP BY decision_type ORDER BY decision_type'

    def summarize(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        return {"decision_types": len(rows), "decisions": sum(int(r.get("decisions",0) or 0) for r in rows), "average_confidence": round(sum(float(r.get("confidence",0) or 0) for r in rows)/len(rows),4) if rows else 0.0}
