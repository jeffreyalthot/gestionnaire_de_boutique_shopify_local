from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class CustomerAddress:
    id: str
    customer_id: str
    encrypted_payload: str
