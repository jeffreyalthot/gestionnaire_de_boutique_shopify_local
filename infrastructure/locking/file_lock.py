from __future__ import annotations

import json
import os
import socket
import time
from pathlib import Path

class FileLock:
    """Verrou exclusif portable fondé sur une création atomique de fichier."""
    def __init__(self, path: Path, *, stale_after_seconds: float = 3600.0) -> None:
        self.path = Path(path)
        self.stale_after_seconds = stale_after_seconds
        self._owned = False

    def _owner_payload(self) -> dict[str, object]:
        return {"pid": os.getpid(), "host": socket.gethostname(), "created_at": time.time()}

    def _is_stale(self) -> bool:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            created_at = float(data.get("created_at", self.path.stat().st_mtime))
        except Exception:
            try:
                created_at = self.path.stat().st_mtime
            except FileNotFoundError:
                return False
        return self.stale_after_seconds > 0 and time.time() - created_at > self.stale_after_seconds

    def acquire(self, timeout: float = 0.0, poll_interval: float = 0.05) -> None:
        deadline = time.monotonic() + max(0.0, timeout)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        while True:
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                try:
                    os.write(fd, json.dumps(self._owner_payload(), sort_keys=True).encode("utf-8"))
                finally:
                    os.close(fd)
                self._owned = True
                return
            except FileExistsError:
                if self._is_stale():
                    try:
                        self.path.unlink()
                    except FileNotFoundError:
                        pass
                    continue
                if time.monotonic() >= deadline:
                    raise RuntimeError(f"Verrou déjà détenu: {self.path}")
                time.sleep(max(0.001, poll_interval))

    def release(self) -> None:
        if not self._owned:
            return
        try:
            self.path.unlink()
        finally:
            self._owned = False

    def __enter__(self) -> "FileLock":
        self.acquire()
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.release()
