from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class ShippingQuote:
    id: str
    supplier_product_id: str
    destination_country: str
    amount: Decimal
    currency: str
    expires_at: datetime
