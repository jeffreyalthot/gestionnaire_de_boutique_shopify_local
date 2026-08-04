from __future__ import annotations

import re
from datetime import datetime, timezone

from finance.financial_snapshot import FinancialSnapshotBuilder
from infrastructure.database.engine import Database

_MONTH = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")


def monthly_close(db: Database, month: str) -> dict[str, object]:
    if not _MONTH.match(month):
        raise ValueError("month must use YYYY-MM")
    snapshot = FinancialSnapshotBuilder().build(db).as_dict()
    previous = db.get_value(f"monthly_close:{month}")
    result = {
        "month": month,
        "financial": db.financial_snapshot(),
        "normalized": snapshot,
        "counts": db.counts(),
        "revision": int(previous.get("revision", 0)) + 1 if isinstance(previous, dict) else 1,
        "closed_at": datetime.now(timezone.utc).isoformat(),
    }
    db.set_value(f"monthly_close:{month}", result)
    db.insert_audit("finance.monthly_close", "finance", {"month": month, "revision": result["revision"]})
    return result
