from __future__ import annotations

from threading import RLock, get_ident


class TerminalSessionOwner:
    """Garantie qu'un seul composant écrit dans la console active."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._owner: int | None = None
        self._depth = 0

    def acquire(self) -> None:
        identity = get_ident()
        self._lock.acquire()
        if self._owner not in (None, identity):
            self._lock.release()
            raise RuntimeError("La session terminal possède déjà un propriétaire.")
        self._owner = identity
        self._depth += 1

    def release(self) -> None:
        identity = get_ident()
        if self._owner != identity or self._depth <= 0:
            raise RuntimeError("Libération terminal par un non-propriétaire.")
        self._depth -= 1
        if self._depth == 0:
            self._owner = None
        self._lock.release()

    @property
    def owned(self) -> bool:
        return self._owner is not None
