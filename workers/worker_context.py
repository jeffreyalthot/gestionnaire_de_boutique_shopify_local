from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from config.settings import Settings
from infrastructure.database.engine import Database
from infrastructure.queue.durable_queue import DurableQueue


@dataclass(slots=True)
class WorkerContext:
    settings: Settings
    db: Database
    queue: DurableQueue
    services: dict[str, object]
    worker_id: str = ""
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def service(self, name: str, *, required: bool = True) -> Any:
        value = self.services.get(name)
        if value is None and required: raise KeyError(f"Service worker absent: {name}")
        return value

    def snapshot(self) -> dict[str, object]:
        return {"worker_id": self.worker_id, "started_at": self.started_at, "services": sorted(self.services), "profile": getattr(self.settings, "runtime_profile", "unknown")}
