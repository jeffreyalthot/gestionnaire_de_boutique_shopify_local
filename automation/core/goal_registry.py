from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Goal:
    name: str
    metric: str
    target: float
    direction: str = "maximize"
    weight: float = 1.0
    enabled: bool = True

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class GoalRegistry:
    def __init__(self) -> None:
        self._goals: dict[str, Goal] = {}

    def register(self, goal: Goal) -> None:
        if goal.direction not in {"maximize", "minimize", "maintain"}:
            raise ValueError("Direction de but invalide.")
        if goal.weight < 0:
            raise ValueError("Le poids ne peut pas être négatif.")
        if goal.name in self._goals:
            raise ValueError(f"But déjà enregistré: {goal.name}")
        self._goals[goal.name] = goal

    def active(self) -> tuple[Goal, ...]:
        return tuple(sorted((g for g in self._goals.values() if g.enabled), key=lambda g: (-g.weight, g.name)))

    def progress(self, metrics: dict[str, float]) -> dict[str, float]:
        result: dict[str, float] = {}
        for goal in self.active():
            current = float(metrics.get(goal.metric, 0.0))
            if goal.direction == "maximize":
                score = current / goal.target if goal.target else 1.0
            elif goal.direction == "minimize":
                score = goal.target / current if current > 0 else 1.0
            else:
                score = 1.0 - abs(current - goal.target) / max(abs(goal.target), 1.0)
            result[goal.name] = max(0.0, min(1.0, score))
        return result
