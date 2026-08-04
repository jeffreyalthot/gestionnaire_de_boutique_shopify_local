from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class ReconciliationCheckpoint:
    id: str
    source: str
    cursor: str
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
