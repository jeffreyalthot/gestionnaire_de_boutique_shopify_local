from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class ProfitSnapshot:
    id: str
    revenue: Decimal
    expenses: Decimal
    gross_profit: Decimal
    net_profit: Decimal
