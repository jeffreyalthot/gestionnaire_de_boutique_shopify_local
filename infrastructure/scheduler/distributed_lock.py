from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from infrastructure.locking.resource_lock import ResourceLockRegistry


class DistributedLock(ResourceLockRegistry):
    """Verrou de planification local, nommable et compatible mono-instance.

    Le nom indique explicitement que cette implémentation ne prétend pas fournir
    de consensus entre plusieurs machines; elle protège le déploiement Windows
    mono-instance ciblé par le projet.
    """

    def __init__(self, namespace: str = "scheduler", *, maximum_locks: int = 4096) -> None:
        super().__init__(maximum_locks=maximum_locks)
        self.namespace = str(namespace).strip() or "scheduler"

    def qualified_name(self, name: str) -> str:
        return f"{self.namespace}:{str(name).strip()}"

    @asynccontextmanager
    async def job(self, name: str, *, timeout: float | None = None) -> AsyncIterator[object]:
        async with self.hold(self.qualified_name(name), timeout=timeout) as lock:
            yield lock
