from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True, slots=True)
class MetricSnapshot:
    values: dict[str, float] = field(default_factory=dict)
    observed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    types: dict[str, str] = field(default_factory=dict)
    labels: dict[str, dict[str, str]] = field(default_factory=dict)

    def as_dict(self) -> dict[str, object]:
        return asdict(self)

    def get(self, name: str, default: float = 0.0) -> float:
        return float(self.values.get(name, default))
