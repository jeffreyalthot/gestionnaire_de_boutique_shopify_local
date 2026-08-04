from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class DecisionScore:
    score: float
    threshold: float
    accepted: bool
    confidence: float
    contributions: dict[str, float] = field(default_factory=dict)
    reason: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
