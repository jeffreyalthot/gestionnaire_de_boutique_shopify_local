from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Any


@dataclass(frozen=True, slots=True)
class RecoveryStep:
    name: str
    execute: Callable[[dict[str, Any]], dict[str, Any]]
    required: bool = True


class RecoveryPlaybook:
    def __init__(self, name: str, steps: tuple[RecoveryStep, ...]) -> None:
        self.name = name
        self.steps = steps

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        results: list[dict[str, Any]] = []
        status = "completed"
        for step in self.steps:
            try:
                output = step.execute(context)
                results.append({"step": step.name, "status": "completed", "output": output})
            except Exception as exc:
                results.append({"step": step.name, "status": "failed", "error": f"{type(exc).__name__}: {exc}"[:500]})
                if step.required:
                    status = "failed"
                    break
                status = "partial"
        return {"name": self.name, "status": status, "steps": tuple(results)}
