from __future__ import annotations

from threading import RLock


class EmergencyLockdown:
    def __init__(self) -> None: self._active=False; self._reason=""; self._lock=RLock()
    def activate(self, reason: str) -> None:
        with self._lock: self._active=True; self._reason=reason[:500]
    def clear(self, *, authorized: bool) -> None:
        if not authorized: raise PermissionError("autorisation requise")
        with self._lock: self._active=False; self._reason=""
    def assert_allowed(self) -> None:
        if self._active: raise RuntimeError(f"runtime verrouillé: {self._reason}")
    def snapshot(self) -> dict[str,object]: return {"active":self._active,"reason":self._reason}
