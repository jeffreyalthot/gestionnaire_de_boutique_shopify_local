from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class ShutdownReport:
    reason: str
    pending_tasks: int
    leased_tasks: int
    failed_tasks: int
    audit_chain_ok: bool
    created_at: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_shutdown_report(container: Any, reason: str = "operator") -> ShutdownReport:
    queue = container.queue.stats()
    audit = container.db.verify_audit_chain()
    return ShutdownReport(
        reason,
        int(queue.get("pending", 0)),
        int(queue.get("leased", 0)),
        int(queue.get("dead", 0)),
        bool(audit.get("ok")),
        datetime.now(timezone.utc).isoformat(),
    )
