from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class WorkflowDefinition:
    name: str
    operations: tuple[str, ...]
    trigger: str
    enabled: bool = True
    description: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class WorkflowCatalog:
    def __init__(self) -> None:
        self._workflows: dict[str, WorkflowDefinition] = {}

    def register(self, workflow: WorkflowDefinition) -> None:
        if not workflow.operations:
            raise ValueError("Un workflow doit contenir au moins une opération.")
        if workflow.name in self._workflows:
            raise ValueError(f"Workflow déjà enregistré: {workflow.name}")
        self._workflows[workflow.name] = workflow

    def enabled(self) -> tuple[WorkflowDefinition, ...]:
        return tuple(self._workflows[key] for key in sorted(self._workflows) if self._workflows[key].enabled)

    def get(self, name: str) -> WorkflowDefinition:
        return self._workflows[name]
