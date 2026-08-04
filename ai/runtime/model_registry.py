from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from threading import RLock
from typing import Any


@dataclass(frozen=True, slots=True)
class ModelDescriptor:
    name: str
    model_type: str
    registered_at: str
    metadata: dict[str, object]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class ModelRegistry:
    def __init__(self) -> None:
        self._models: dict[str, object] = {}
        self._descriptors: dict[str, ModelDescriptor] = {}
        self._lock = RLock()

    def register(self, name: str, model: object, *, metadata: dict[str, object] | None = None, replace: bool = True) -> None:
        name = str(name).strip()
        if not name:
            raise ValueError("model name is required")
        with self._lock:
            if name in self._models and not replace:
                raise ValueError(f"model already registered: {name}")
            self._models[name] = model
            self._descriptors[name] = ModelDescriptor(name, f"{type(model).__module__}.{type(model).__qualname__}", datetime.now(timezone.utc).isoformat(), dict(metadata or {}))

    def get(self, name: str) -> object:
        with self._lock:
            return self._models[name]

    def unload(self, name: str) -> bool:
        with self._lock:
            removed = self._models.pop(name, None) is not None
            self._descriptors.pop(name, None)
            return removed

    def names(self) -> list[str]:
        with self._lock:
            return sorted(self._models)

    def descriptors(self) -> tuple[dict[str, object], ...]:
        with self._lock:
            return tuple(self._descriptors[name].as_dict() for name in sorted(self._descriptors))

    def snapshot(self) -> dict[str, object]:
        return {"count": len(self.names()), "models": self.descriptors()}
