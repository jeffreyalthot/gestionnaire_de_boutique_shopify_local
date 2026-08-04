from __future__ import annotations

from datetime import date, datetime, timezone

from finance.financial_snapshot import FinancialSnapshotBuilder
from infrastructure.database.engine import Database


def daily_close(db: Database, close_date: str | None = None) -> dict[str, object]:
    day = close_date or date.today().isoformat()
    snapshot = FinancialSnapshotBuilder().build(db).as_dict()
    audit = db.verify_audit_chain()
    result = {
        "date": day,
        "financial": db.financial_snapshot(),
        "normalized": snapshot,
        "counts": db.counts(),
        "audit": audit,
        "closed_at": datetime.now(timezone.utc).isoformat(),
    }
    db.set_value(f"daily_close:{day}", result)
    db.set_value("last_daily_close", result)
    db.insert_audit("finance.daily_close", "finance", {"date": day, "audit_valid": bool(audit.get("valid", False))})
    return result
