from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class Customer:
    id: str
    email: str
    first_name: str = ""
    last_name: str = ""
