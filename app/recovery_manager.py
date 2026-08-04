from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class RecoveryReport:
    recovered_leases: int
    resumed_checkpoints: int
    dead_tasks: int
    database_ok: bool
    audit_ok: bool
    created_at: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class RecoveryManager:
    def __init__(self, db: Any, queue: Any) -> None:
        self.db = db
        self.queue = queue

    def recover(self) -> RecoveryReport:
        recovered = int(self.db.purge_expired_leases())
        checkpoints = int(self.db.scalar(
            "SELECT COUNT(*) FROM reconciliation_checkpoints WHERE status IN ('running','failed')", default=0
        ))
        dead = int(self.db.scalar("SELECT COUNT(*) FROM tasks WHERE status='dead'", default=0))
        health = self.db.health()
        audit = self.db.verify_audit_chain()
        report = RecoveryReport(
            recovered, checkpoints, dead, bool(health.get("ok")), bool(audit.get("ok")),
            datetime.now(timezone.utc).isoformat(),
        )
        self.db.insert_audit("runtime.recovery", "recovery-manager", report.as_dict())
        return report
