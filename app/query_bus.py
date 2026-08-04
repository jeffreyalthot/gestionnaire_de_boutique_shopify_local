from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable
from typing import Any

QueryHandler = Callable[[dict[str, Any]], Any | Awaitable[Any]]


class QueryBus:
    """Bus de lecture sans effet de bord, borné et introspectable."""

    def __init__(self) -> None:
        self._handlers: dict[str, QueryHandler] = {}
        self._calls: dict[str, int] = {}

    def register(self, name: str, handler: QueryHandler) -> None:
        key = name.strip().lower()
        if not key:
            raise ValueError("Le nom de requête est requis.")
        if key in self._handlers:
            raise ValueError(f"Requête déjà enregistrée: {key}")
        self._handlers[key] = handler
        self._calls[key] = 0

    async def ask(self, name: str, payload: dict[str, Any] | None = None) -> Any:
        key = name.strip().lower()
        if key not in self._handlers:
            raise KeyError(f"Requête inconnue: {key}")
        self._calls[key] += 1
        result = self._handlers[key](dict(payload or {}))
        return await result if inspect.isawaitable(result) else result

    def snapshot(self) -> dict[str, Any]:
        return {"registered": tuple(sorted(self._handlers)), "calls": dict(self._calls)}
