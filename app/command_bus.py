from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

Handler = Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]


class CommandBus:
    def __init__(self) -> None:
        self._handlers: dict[str, Handler] = {}

    def register(self, name: str, handler: Handler) -> None:
        if name in self._handlers:
            raise ValueError(f"Commande déjà enregistrée: {name}")
        self._handlers[name] = handler

    async def dispatch(self, name: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        if name not in self._handlers:
            raise KeyError(name)
        return await self._handlers[name](payload or {})

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._handlers))
