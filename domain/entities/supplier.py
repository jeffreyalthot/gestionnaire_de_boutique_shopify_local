from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class Supplier:
    id: str
    name: str
    score: float = 0.0
    status: str = "unknown"
