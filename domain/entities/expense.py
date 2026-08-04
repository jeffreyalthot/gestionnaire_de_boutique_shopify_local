from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class Expense:
    id: str
    category: str
    amount: Decimal
    currency: str = "CAD"
