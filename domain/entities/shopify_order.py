from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class ShopifyOrder:
    id: str
    name: str
    total_cad: Decimal
    payment_status: str
    fulfillment_status: str
