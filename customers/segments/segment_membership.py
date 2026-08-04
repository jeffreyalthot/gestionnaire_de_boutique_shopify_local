from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class SegmentMembership:
    customer_id: str
    segment: str
    score: float
    reason: str
    updated_at: str = ""

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        if not data["updated_at"]:
            data["updated_at"] = datetime.now(timezone.utc).isoformat()
        return data
