from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class SupplierOrder:
    id: str
    batch_id: str
    supplier_id: str
    external_order_id: str = ""
    status: str = "pending"
