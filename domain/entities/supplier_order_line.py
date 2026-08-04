from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class SupplierOrderLine:
    id: str
    supplier_order_id: str
    supplier_sku_id: str
    quantity: int
    unit_cost: Decimal
