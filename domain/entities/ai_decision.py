from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class AIDecision:
    id: str
    decision_type: str
    confidence: float
    payload: dict[str, object]
