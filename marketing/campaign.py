from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Campaign:
    id: str
    name: str
    channel: str
    budget_cad: float
    starts_at: datetime
    ends_at: datetime
    status: str="draft"
    audience: tuple[str,...]=field(default_factory=tuple)
