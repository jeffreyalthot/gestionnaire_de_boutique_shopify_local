from __future__ import annotations

import inspect
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable

HealthProbe = Callable[[], Any]


@dataclass(frozen=True, slots=True)
class ProbeDefinition:
    name: str
    probe: HealthProbe
    critical: bool = False


class HealthAggregator:
    def __init__(self) -> None:
        self._probes: dict[str, ProbeDefinition] = {}

    def register(self, name: str, probe: HealthProbe, *, critical: bool = False) -> None:
        key = name.strip().lower()
        if not key:
            raise ValueError("Le nom de sonde est requis.")
        if key in self._probes:
            raise ValueError(f"Sonde déjà enregistrée: {key}")
        self._probes[key] = ProbeDefinition(key, probe, critical)

    async def collect(self) -> dict[str, Any]:
        details: dict[str, Any] = {}
        critical_failures: list[str] = []
        warnings: list[str] = []
        for key in sorted(self._probes):
            definition = self._probes[key]
            try:
                value = definition.probe()
                if inspect.isawaitable(value):
                    value = await value
                normalized = value if isinstance(value, dict) else {"ok": bool(value), "value": value}
                ok = bool(normalized.get("ok", True))
                details[key] = {**normalized, "critical": definition.critical}
                if not ok:
                    (critical_failures if definition.critical else warnings).append(key)
            except Exception as exc:
                details[key] = {"ok": False, "critical": definition.critical, "error": f"{type(exc).__name__}: {exc}"[:500]}
                (critical_failures if definition.critical else warnings).append(key)
        status = "unhealthy" if critical_failures else ("degraded" if warnings else "healthy")
        return {
            "ok": not critical_failures,
            "status": status,
            "critical_failures": tuple(critical_failures),
            "warnings": tuple(warnings),
            "probes": details,
            "collected_at": datetime.now(timezone.utc).isoformat(),
        }
