from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class DashboardRuntimeSnapshot:
    captured_at: str
    page: str
    lines: tuple[str, ...]
    state: dict[str, Any]

    @classmethod
    def capture(cls, page: str, lines: list[str], state: dict[str, Any]) -> 'DashboardRuntimeSnapshot':
        return cls(datetime.now(timezone.utc).isoformat(), page, tuple(lines), dict(state))

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
