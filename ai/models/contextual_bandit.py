from __future__ import annotations

import math
import random
from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class BanditSnapshot:
    counts: dict[str, int]
    values: dict[str, float]
    total_observations: int
    exploration: float = 1.5

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class ContextualBandit:
    """Bandit UCB1 déterministe, borné et sérialisable."""

    def __init__(self, actions: list[str], exploration: float = 1.5, seed: int = 42) -> None:
        normalized = [str(action).strip() for action in actions]
        if not normalized or any(not action for action in normalized) or len(set(normalized)) != len(normalized):
            raise ValueError("actions uniques requises")
        self.actions = tuple(normalized)
        self.exploration = max(0.0, float(exploration))
        self.counts = {action: 0 for action in self.actions}
        self.values = {action: 0.0 for action in self.actions}
        self._rng = random.Random(seed)

    @staticmethod
    def _bounded(value: Any) -> float:
        try:
            number = float(value)
        except (TypeError, ValueError):
            return 0.0
        return max(-1.0, min(1.0, number if math.isfinite(number) else 0.0))

    def scores(self, context_scores: Mapping[str, float] | None = None) -> dict[str, float]:
        context = context_scores or {}
        total = max(1, sum(self.counts.values()))
        result: dict[str, float] = {}
        for action in self.actions:
            if self.counts[action] == 0:
                result[action] = float("inf")
            else:
                result[action] = (
                    self.values[action]
                    + self._bounded(context.get(action, 0.0))
                    + self.exploration * math.sqrt(math.log(total) / self.counts[action])
                )
        return result

    def choose(self, context_scores: dict[str, float] | None = None, *, allowed_actions: set[str] | None = None) -> str:
        candidates = tuple(action for action in self.actions if allowed_actions is None or action in allowed_actions)
        if not candidates:
            raise ValueError("no_allowed_actions")
        untried = [action for action in candidates if self.counts[action] == 0]
        if untried:
            return self._rng.choice(untried)
        scores = self.scores(context_scores)
        return max(candidates, key=lambda action: (scores[action], -self.actions.index(action)))

    def update(self, action: str, reward: float, *, weight: float = 1.0) -> None:
        if action not in self.counts:
            raise KeyError(action)
        bounded_reward = self._bounded(reward)
        weight_value = max(0.0, min(1000.0, float(weight)))
        if weight_value == 0.0:
            return
        previous_count = self.counts[action]
        increment = max(1, int(round(weight_value)))
        new_count = previous_count + increment
        self.values[action] = (self.values[action] * previous_count + bounded_reward * increment) / new_count
        self.counts[action] = new_count

    def snapshot(self) -> BanditSnapshot:
        return BanditSnapshot(dict(self.counts), dict(self.values), sum(self.counts.values()), self.exploration)

    def restore(self, snapshot: BanditSnapshot | Mapping[str, Any]) -> None:
        data = snapshot.as_dict() if isinstance(snapshot, BanditSnapshot) else dict(snapshot)
        counts = dict(data.get("counts", {}))
        values = dict(data.get("values", {}))
        if set(counts) != set(self.actions) or set(values) != set(self.actions):
            raise ValueError("bandit_actions_mismatch")
        self.counts = {action: max(0, int(counts[action])) for action in self.actions}
        self.values = {action: self._bounded(values[action]) for action in self.actions}
        self.exploration = max(0.0, float(data.get("exploration", self.exploration)))
