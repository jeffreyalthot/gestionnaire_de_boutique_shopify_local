from __future__ import annotations

from typing import Iterable


class LightweightRanker:
    """Classement O(n log n), sans NumPy, borné à quelques centaines d'éléments."""

    def __init__(self, weights: dict[str, float] | None = None) -> None:
        self.weights = dict(weights or {})

    def score(self, features: dict[str, float]) -> float:
        if not features:
            return 0.0
        if self.weights:
            numerator = sum(max(0.0, min(1.0, float(features.get(key, 0.0)))) * weight
                            for key, weight in self.weights.items())
            denominator = sum(abs(weight) for weight in self.weights.values()) or 1.0
        else:
            numerator = sum(max(0.0, min(1.0, float(value))) for value in features.values())
            denominator = float(len(features))
        return max(0.0, min(1.0, numerator / denominator))

    def rank(self, items: Iterable[tuple[str, dict[str, float]]], *, limit: int | None = None) -> tuple[tuple[str, float], ...]:
        ranked = sorted(((key, self.score(features)) for key, features in items), key=lambda item: (-item[1], item[0]))
        return tuple(ranked if limit is None else ranked[: max(0, limit)])
