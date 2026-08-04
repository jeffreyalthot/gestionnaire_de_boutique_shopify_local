from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class ApiEvent:
    id: str
    source: str
    topic: str
    payload: dict[str, object]
