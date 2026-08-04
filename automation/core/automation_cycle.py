from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from automation.core.automation_context import AutomationContext


@dataclass(slots=True)
class CycleReport:
    cycle_id: str
    started_at: str
    finished_at: str = ""
    planned: int = 0
    accepted: int = 0
    rejected: int = 0
    completed: int = 0
    failed: int = 0
    deferred: int = 0
    operations: list[dict[str, Any]] = field(default_factory=list)

    def finish(self) -> "CycleReport":
        self.finished_at = datetime.now(timezone.utc).isoformat()
        return self

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class AutomationCycle:
    def __init__(self, context: AutomationContext) -> None:
        self.context = context
        self.report = CycleReport(context.cycle_id, context.started_at)
