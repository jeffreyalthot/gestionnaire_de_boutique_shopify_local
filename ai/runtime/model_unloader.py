from __future__ import annotations

import gc
from dataclasses import dataclass
from time import monotonic
from typing import Any, MutableMapping


@dataclass(frozen=True, slots=True)
class UnloadResult:
    name: str
    removed: bool
    collected_objects: int
    duration_ms: float
    cleanup_called: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "removed": self.removed,
            "collected_objects": self.collected_objects,
            "duration_ms": self.duration_ms,
            "cleanup_called": self.cleanup_called,
        }


def unload_model(registry: MutableMapping[str, object], name: str, *, collect: bool = True) -> UnloadResult:
    """Retire un modèle et appelle son hook de fermeture lorsqu'il existe."""
    started = monotonic()
    model = registry.pop(name, None)
    cleanup_called = False
    if model is not None:
        for method_name in ("close", "shutdown", "unload"):
            method = getattr(model, method_name, None)
            if callable(method):
                method()
                cleanup_called = True
                break
    collected = gc.collect() if collect else 0
    return UnloadResult(
        name=str(name),
        removed=model is not None,
        collected_objects=int(collected),
        duration_ms=round((monotonic() - started) * 1000.0, 3),
        cleanup_called=cleanup_called,
    )


def unload_reference(registry: dict[str, object], name: str) -> None:
    """API historique conservée."""
    unload_model(registry, name)


def unload_all(registry: MutableMapping[str, object], *, collect_each: bool = False) -> tuple[UnloadResult, ...]:
    results = [unload_model(registry, name, collect=collect_each) for name in tuple(registry)]
    if not collect_each:
        gc.collect()
    return tuple(results)
