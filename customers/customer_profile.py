from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class CustomerProfile:
    customer_id: str
    email_hash: str = ""
    country_code: str = ""
    language: str = ""
    lifetime_value_cad: float = 0.0
    risk_score: float = 0.0
    preferences: dict[str, Any] = field(default_factory=dict)
    tags: tuple[str, ...] = ()
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
