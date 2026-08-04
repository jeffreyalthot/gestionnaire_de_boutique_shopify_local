from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Callable, Iterable
from uuid import uuid4

from automation.reconciliation.base_reconciler import BaseReconciler, KeySelector, ReconciliationReport


class PersistentReconciler(BaseReconciler):
    """Base reconciler that persists run history and a restart cursor."""

    default_key: KeySelector = "id"
    ignored_fields: tuple[str, ...] = ("updated_at", "created_at")

    def __init__(self, entity: str, db: Any, *, maximum_differences: int = 500) -> None:
        super().__init__(entity, maximum_differences=maximum_differences)
        self.db = db

    def run(
        self,
        local_items: Iterable[dict[str, Any]],
        remote_items: Iterable[dict[str, Any]],
        *,
        key: KeySelector | None = None,
        repair: Callable[[dict[str, Any], dict[str, Any]], bool] | None = None,
        create_local: Callable[[dict[str, Any]], bool] | None = None,
        create_remote: Callable[[dict[str, Any]], bool] | None = None,
        ignore_fields: Iterable[str] | None = None,
        compare_fields: Iterable[str] | None = None,
        numeric_tolerance: float = 0.0,
        cursor: str | None = None,
    ) -> ReconciliationReport:
        identifier = str(uuid4())
        started = datetime.now(timezone.utc).isoformat()
        report = self.reconcile(
            local_items,
            remote_items,
            key=self.default_key if key is None else key,
            repair=repair,
            create_local=create_local,
            create_remote=create_remote,
            ignore_fields=self.ignored_fields if ignore_fields is None else ignore_fields,
            compare_fields=compare_fields,
            numeric_tolerance=numeric_tolerance,
        )
        status = "completed" if report.ok else "partial"
        finished = datetime.now(timezone.utc).isoformat()
        detail = json.dumps(report.as_dict(), ensure_ascii=False, default=str, separators=(",", ":"))
        self.db.execute(
            "INSERT INTO reconciliation_runs(id,name,status,scanned,matched,drifted,repaired,detail_json,started_at,finished_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
            (identifier, self.entity, status, report.checked, report.matched, report.drifted, report.repaired, detail, started, finished),
        )
        checkpoint = cursor or finished
        self.db.execute(
            "INSERT INTO reconciliation_checkpoints(name,cursor,status,detail_json,updated_at) VALUES(?,?,?,?,?) "
            "ON CONFLICT(name) DO UPDATE SET cursor=excluded.cursor,status=excluded.status,detail_json=excluded.detail_json,updated_at=excluded.updated_at",
            (self.entity, checkpoint, status, detail, finished),
        )
        return report

    def last_checkpoint(self) -> dict[str, Any] | None:
        row = self.db.query_one("SELECT * FROM reconciliation_checkpoints WHERE name=?", (self.entity,))
        return dict(row) if row else None

    def recent_runs(self, limit: int = 20) -> list[dict[str, Any]]:
        return list(self.db.query(
            "SELECT * FROM reconciliation_runs WHERE name=? ORDER BY started_at DESC LIMIT ?",
            (self.entity, max(1, min(int(limit), 500))),
        ))
