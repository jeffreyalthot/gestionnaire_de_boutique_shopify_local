from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(slots=True)
class Ticket:
    category: str
    subject: str
    order_id: str = ""
    customer_id: str = ""
    priority: int = 100
    status: str = "open"
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def as_dict(self) -> dict[str, object]:
        return asdict(self)
