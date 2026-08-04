from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class Fulfillment:
    id: str
    shopify_order_id: str
    shopify_fulfillment_id: str = ""
    status: str = "pending"
