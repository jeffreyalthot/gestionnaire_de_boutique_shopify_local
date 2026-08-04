from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class LedgerEntry:
    id: str
    account: str
    debit: Decimal
    credit: Decimal
    currency: str = "CAD"
