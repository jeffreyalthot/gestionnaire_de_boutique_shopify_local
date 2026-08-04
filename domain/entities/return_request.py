from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class ReturnRequest:
    id: str
    order_id: str
    status: str
    reason: str = ""
