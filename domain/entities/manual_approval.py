from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class ManualApproval:
    id: str
    action: str
    status: str
    requested_amount: Decimal = Decimal("0")
