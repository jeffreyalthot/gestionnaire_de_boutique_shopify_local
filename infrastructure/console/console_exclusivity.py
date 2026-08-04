from __future__ import annotations
import threading


class ConsoleExclusivity:
    """Garantit qu'un seul composant interactif possède stdout/stderr."""
    _lock = threading.RLock()
    _owner: str | None = None

    def acquire(self, owner: str) -> bool:
        with self._lock:
            if self._owner not in (None, owner):
                return False
            self._owner = owner
            return True

    def release(self, owner: str) -> None:
        with self._lock:
            if self._owner == owner:
                self._owner = None

    @property
    def owner(self) -> str | None:
        with self._lock:
            return self._owner
