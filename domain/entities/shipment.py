from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class Shipment:
    id: str
    supplier_order_id: str
    carrier: str
    tracking_number: str
    status: str
