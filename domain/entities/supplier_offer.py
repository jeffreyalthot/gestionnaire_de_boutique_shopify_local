from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class SupplierOffer:
    id: str
    supplier_id: str
    product_id: str
    unit_cost: Decimal
    currency: str
    minimum_quantity: int = 1
