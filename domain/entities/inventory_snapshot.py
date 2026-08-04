from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class InventorySnapshot:
    id: str
    sku: str
    quantity: int
    captured_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
