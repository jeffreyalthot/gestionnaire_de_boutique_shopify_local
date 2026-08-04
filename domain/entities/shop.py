from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class Shop:
    id: str
    domain: str
    currency: str = "CAD"
    enabled: bool = True
