from dataclasses import dataclass,field
from datetime import datetime,timezone
from typing import Any
@dataclass(slots=True)
class ProductRecord:
    id: str
    data: dict[str,Any]=field(default_factory=dict)
    created_at: str=field(default_factory=lambda:datetime.now(timezone.utc).isoformat())
