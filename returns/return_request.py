from dataclasses import dataclass,field
from datetime import datetime,timezone


@dataclass(frozen=True, slots=True)
class ReturnRequest:
    id: str
    order_id: str
    reason: str
    items: tuple[dict[str,object],...]=field(default_factory=tuple)
    requested_at: datetime=field(default_factory=lambda:datetime.now(timezone.utc))
    status: str="requested"
