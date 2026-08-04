from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class WorkerDescriptor:
    name: str
    queue: str
    task_types: tuple[str, ...]
    heavy: bool = False


class WorkerRegistry:
    def __init__(self) -> None:
        self._workers: dict[str, tuple[WorkerDescriptor, Any]] = {}

    def register(self, descriptor: WorkerDescriptor, worker: Any) -> None:
        if descriptor.name in self._workers:
            raise ValueError(f'Worker déjà enregistré: {descriptor.name}')
        self._workers[descriptor.name] = (descriptor, worker)

    def get(self, name: str) -> Any:
        return self._workers[name][1]

    def descriptors(self) -> tuple[WorkerDescriptor, ...]:
        return tuple(item[0] for item in self._workers.values())

    def task_routes(self) -> dict[str, str]:
        routes: dict[str, str] = {}
        for descriptor, _ in self._workers.values():
            for task_type in descriptor.task_types:
                if task_type in routes:
                    raise ValueError(f'Tâche routée deux fois: {task_type}')
                routes[task_type] = descriptor.name
        return routes
