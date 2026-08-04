from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class AutomationContext:
    cycle_id: str = field(default_factory=lambda: str(uuid4()))
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    dry_run: bool = True
    mode: str = "supervised"
    metadata: dict[str, Any] = field(default_factory=dict)

    def child_metadata(self, **values: Any) -> dict[str, Any]:
        return {"cycle_id": self.cycle_id, "dry_run": self.dry_run, "mode": self.mode, **self.metadata, **values}
