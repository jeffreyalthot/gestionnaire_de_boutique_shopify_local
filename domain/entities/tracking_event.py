from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class TrackingEvent:
    id: str
    shipment_id: str
    status: str
    description: str
    occurred_at: datetime
