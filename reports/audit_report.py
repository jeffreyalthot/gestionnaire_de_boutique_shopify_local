from __future__ import annotations

from typing import Any

from reports.report_base import QueryReport, aggregate, ratio, grouped_summary


class AuditReport(QueryReport):
    name = 'audit'
    query = 'SELECT id,action,actor,detail_json,created_at,previous_hash,entry_hash FROM audit_log ORDER BY created_at DESC'

    def summarize(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        return {"entries": len(rows), "actors": len({str(r.get("actor","")) for r in rows}), "actions": grouped_summary(rows,"action")}
