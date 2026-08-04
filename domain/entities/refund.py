from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class Refund:
    id: str
    order_id: str
    amount: Decimal
    reason: str = ""
