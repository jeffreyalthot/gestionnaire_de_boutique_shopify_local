from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass
from time import monotonic
from typing import AsyncIterator


@dataclass(slots=True)
class _LockEntry:
    lock: asyncio.Lock
    users: int = 0
    acquisitions: int = 0
    wait_seconds: float = 0.0


class ResourceLockRegistry:
    """Registre de verrous asyncio borné avec nettoyage des ressources inactives."""

    def __init__(self, *, maximum_locks: int = 4096) -> None:
        self.maximum_locks = max(16, int(maximum_locks))
        self._entries: dict[str, _LockEntry] = {}
        self._guard = asyncio.Lock()

    @staticmethod
    def _name(name: str) -> str:
        value = str(name).strip()
        if not value or len(value) > 256 or any(character in value for character in "\r\n\0"):
            raise ValueError("resource_lock_name_invalid")
        return value

    def get(self, name: str) -> asyncio.Lock:
        value = self._name(name)
        entry = self._entries.get(value)
        if entry is None:
            if len(self._entries) >= self.maximum_locks:
                self.prune()
            if len(self._entries) >= self.maximum_locks:
                raise RuntimeError("resource_lock_capacity_exceeded")
            entry = _LockEntry(asyncio.Lock())
            self._entries[value] = entry
        return entry.lock

    @asynccontextmanager
    async def hold(self, name: str, *, timeout: float | None = None) -> AsyncIterator[asyncio.Lock]:
        value = self._name(name)
        lock = self.get(value)
        entry = self._entries[value]
        started = monotonic()
        entry.users += 1
        try:
            if timeout is None:
                await lock.acquire()
            else:
                await asyncio.wait_for(lock.acquire(), timeout=max(0.001, float(timeout)))
            entry.acquisitions += 1
            entry.wait_seconds += monotonic() - started
            try:
                yield lock
            finally:
                lock.release()
        finally:
            entry.users = max(0, entry.users - 1)

    def prune(self) -> int:
        removable = [name for name, entry in self._entries.items() if entry.users == 0 and not entry.lock.locked()]
        for name in removable:
            self._entries.pop(name, None)
        return len(removable)

    def statistics(self) -> dict[str, object]:
        return {
            "locks": len(self._entries),
            "locked": sum(entry.lock.locked() for entry in self._entries.values()),
            "users": sum(entry.users for entry in self._entries.values()),
            "acquisitions": sum(entry.acquisitions for entry in self._entries.values()),
            "wait_seconds": round(sum(entry.wait_seconds for entry in self._entries.values()), 6),
            "maximum_locks": self.maximum_locks,
        }
