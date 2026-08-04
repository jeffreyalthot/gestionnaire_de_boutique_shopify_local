from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class ProcurementBatch:
    id: str
    total_cad: Decimal
    status: str = "open"
    order_count: int = 0
