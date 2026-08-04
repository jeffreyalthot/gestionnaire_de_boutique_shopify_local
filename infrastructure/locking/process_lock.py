from __future__ import annotations

from pathlib import Path

from infrastructure.locking.file_lock import FileLock


class ProcessLock:
    """Verrou de processus récupérable après un arrêt brutal."""

    def __init__(self, path: Path, *, stale_after_seconds: float = 86_400.0) -> None:
        self.path = Path(path)
        self._lock = FileLock(self.path, stale_after_seconds=stale_after_seconds)

    def acquire(self, timeout: float = 0.0) -> None:
        try:
            self._lock.acquire(timeout=timeout)
        except RuntimeError as exc:
            raise RuntimeError("Une instance est déjà active.") from exc

    def release(self) -> None:
        self._lock.release()

    def __enter__(self) -> "ProcessLock":
        self.acquire()
        return self

    def __exit__(self, *_args: object) -> None:
        self.release()
