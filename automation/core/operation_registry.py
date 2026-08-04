from __future__ import annotations

from dataclasses import dataclass
from typing import Awaitable, Callable

OperationHandler = Callable[[], Awaitable[dict[str, object]]]


@dataclass(frozen=True, slots=True)
class OperationDefinition:
    name: str
    capability: str
    queue: str = "default"
    priority: int = 100
    heavy: bool = False
    risk: str = "read_only"
    interval_seconds: int = 300


class OperationRegistry:
    def __init__(self) -> None:
        self._definitions: dict[str, OperationDefinition] = {}

    def register(self, definition: OperationDefinition) -> None:
        if definition.name in self._definitions:
            raise ValueError(f"Opération déjà enregistrée: {definition.name}")
        self._definitions[definition.name] = definition

    def get(self, name: str) -> OperationDefinition:
        return self._definitions[name]

    def all(self) -> tuple[OperationDefinition, ...]:
        return tuple(sorted(self._definitions.values(), key=lambda item: (item.priority, item.name)))
