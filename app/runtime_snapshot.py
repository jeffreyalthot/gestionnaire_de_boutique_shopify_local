from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class RuntimeSnapshot:
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: str = "unknown"
    phase: str = "idle"
    resource: dict[str, Any] = field(default_factory=dict)
    queue: dict[str, int] = field(default_factory=dict)
    automation: dict[str, Any] = field(default_factory=dict)
    integrations: dict[str, Any] = field(default_factory=dict)
    health: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
