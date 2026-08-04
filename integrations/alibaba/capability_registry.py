from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable


@dataclass(slots=True)
class AlibabaCapabilities:
    values: dict[str, bool] = field(default_factory=dict)
    errors: dict[str, str] = field(default_factory=dict)
    checked_at: dict[str, str] = field(default_factory=dict)

    def can(self, name: str) -> bool:
        return bool(self.values.get(str(name), False))

    def update(self, name: str, available: bool, error: str = "") -> None:
        key = str(name)
        self.values[key] = bool(available)
        self.checked_at[key] = datetime.now(timezone.utc).isoformat()
        if error:
            self.errors[key] = str(error)[:1000]
        else:
            self.errors.pop(key, None)

    def require(self, *names: str) -> tuple[str, ...]:
        return tuple(name for name in names if not self.can(name))

    def merge(self, values: dict[str, bool]) -> None:
        for name, available in values.items():
            self.update(name, available)

    def snapshot(self) -> dict[str, object]:
        return {
            "values": dict(sorted(self.values.items())),
            "errors": dict(sorted(self.errors.items())),
            "checked_at": dict(sorted(self.checked_at.items())),
            "available": sum(self.values.values()),
            "total": len(self.values),
        }
