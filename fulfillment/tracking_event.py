from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class TrackingEvent:
    status: str
    description: str
    occurred_at: str
    location: str = ""
    source: str = "supplier"
    received_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def as_dict(self) -> dict[str, Any]: return asdict(self)
