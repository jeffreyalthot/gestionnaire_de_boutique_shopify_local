from __future__ import annotations

from contextlib import contextmanager
from threading import RLock, get_ident
from typing import Iterator


class SingleWriterGuard:
    """Sérialise les mutations d'un agrégat et détecte les sorties non appariées."""

    def __init__(self) -> None:
        self._locks: dict[str, RLock] = {}
        self._owners: dict[str, tuple[int, int]] = {}
        self._registry_lock = RLock()

    @contextmanager
    def acquire(self, resource: str) -> Iterator[None]:
        key = resource.strip()
        if not key:
            raise ValueError("La ressource est requise.")
        with self._registry_lock:
            lock = self._locks.setdefault(key, RLock())
        lock.acquire()
        identity = get_ident()
        owner, depth = self._owners.get(key, (identity, 0))
        if owner != identity:
            lock.release()
            raise RuntimeError(f"Ressource possédée par un autre writer: {key}")
        self._owners[key] = (identity, depth + 1)
        try:
            yield
        finally:
            _, current = self._owners[key]
            if current <= 1:
                self._owners.pop(key, None)
            else:
                self._owners[key] = (identity, current - 1)
            lock.release()

    def active(self) -> tuple[str, ...]:
        return tuple(sorted(self._owners))
