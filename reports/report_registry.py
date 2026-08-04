from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from time import monotonic
from typing import Any, Callable


@dataclass(frozen=True, slots=True)
class ReportRun:
    name: str
    ok: bool
    duration_ms: float
    result: Any = None
    error: str = ""

    def as_dict(self) -> dict[str, object]: return asdict(self)


class ReportRegistry:
    def __init__(self) -> None:
        self._factories: dict[str, Callable[[Any], Any]] = {}; self._runs: list[ReportRun] = []

    def register(self, name: str, factory: Callable[[Any], Any]) -> None:
        key = name.strip().lower()
        if not key or key in self._factories: raise ValueError("rapport invalide ou dupliqué")
        self._factories[key] = factory

    def unregister(self, name: str) -> bool:
        return self._factories.pop(name.strip().lower(), None) is not None

    def names(self) -> tuple[str, ...]: return tuple(sorted(self._factories))

    def generate(self, name: str, db: Any) -> Any:
        key = name.strip().lower(); started = monotonic()
        try:
            report = self._factories[key](db); result = report.generate()
        except Exception as exc:
            run = ReportRun(key, False, round((monotonic() - started) * 1000, 3), error=f"{type(exc).__name__}: {exc}"[:1000]); self._runs.append(run); raise
        run = ReportRun(key, True, round((monotonic() - started) * 1000, 3), result=result); self._runs.append(run); return result

    def bundle(self, names: list[str], db: Any) -> dict[str, object]:
        results: dict[str, object] = {}; errors: dict[str, str] = {}
        for name in dict.fromkeys(names):
            try: results[name] = self.generate(name, db)
            except Exception as exc: errors[name] = f"{type(exc).__name__}: {exc}"[:1000]
        return {"generated_at": datetime.now(timezone.utc).isoformat(), "reports": results, "errors": errors, "ok": not errors, "requested": len(names), "completed": len(results)}

    def stats(self) -> dict[str, object]:
        return {"registered": len(self._factories), "runs": len(self._runs), "failed": sum(not run.ok for run in self._runs), "last": self._runs[-1].as_dict() if self._runs else None}
