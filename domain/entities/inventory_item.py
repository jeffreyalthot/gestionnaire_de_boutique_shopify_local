from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class InventoryItem:
    id: str
    sku: str
    available: int
    reserved: int = 0
