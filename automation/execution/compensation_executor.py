from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True, slots=True)
class Compensation:
    name: str
    handler: Callable[[], Any]
    required: bool = True


class CompensationExecutor:
    async def execute(self, compensations: tuple[Compensation, ...]) -> dict[str, Any]:
        results: list[dict[str, Any]] = []
        status = "completed"
        for item in reversed(compensations):
            try:
                output = item.handler()
                if inspect.isawaitable(output):
                    output = await output
                results.append({"name": item.name, "status": "completed", "output": output})
            except Exception as exc:
                results.append({"name": item.name, "status": "failed", "error": f"{type(exc).__name__}: {exc}"[:500]})
                status = "failed" if item.required else "partial"
                if item.required:
                    break
        return {"status": status, "results": tuple(results)}
