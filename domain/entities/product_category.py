from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class ProductCategory:
    id: str
    name: str
    parent_id: str = ""
