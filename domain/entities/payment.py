from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class Payment:
    id: str
    external_order_id: str
    amount: Decimal
    currency: str
    status: str
