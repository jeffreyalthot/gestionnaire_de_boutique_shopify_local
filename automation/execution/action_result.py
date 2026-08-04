from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class ActionResult:
    name: str
    status: str
    idempotency_key: str
    simulated: bool = False
    reason: str = ""
    output: dict[str, Any] = field(default_factory=dict)
    error: str = ""
    finished_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
