from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class ShopifyOrderLine:
    id: str
    order_id: str
    sku: str
    quantity: int
    unit_price_cad: Decimal
