from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class PaymentAttempt:
    id: str
    payment_id: str
    attempt_number: int
    status: str
    response_code: str = ""
