from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

@dataclass(slots=True)
class AuditEvent:
    id: str
    action: str
    actor: str
    details: dict[str, object]
