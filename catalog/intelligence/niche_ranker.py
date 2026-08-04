from __future__ import annotations

from typing import Iterable


class NicheRanker:
    WEIGHTS = {"demand": 0.30, "profitability": 0.25, "competition": 0.15,
               "saturation": -0.15, "return_risk": -0.10, "compliance": 0.05}

    def score(self, signals: dict[str, float]) -> float:
        positive = sum(max(0.0, min(1.0, signals.get(key, 0.0))) * weight
                       for key, weight in self.WEIGHTS.items() if weight > 0)
        negative = sum(max(0.0, min(1.0, signals.get(key, 0.0))) * abs(weight)
                       for key, weight in self.WEIGHTS.items() if weight < 0)
        denominator = sum(abs(weight) for weight in self.WEIGHTS.values())
        return round(max(0.0, min(1.0, (positive + (sum(abs(w) for w in self.WEIGHTS.values() if w < 0) - negative)) / denominator)), 6)

    def rank(self, niches: Iterable[tuple[str, dict[str, float]]], limit: int = 20) -> tuple[tuple[str, float], ...]:
        return tuple(sorted(((name, self.score(signals)) for name, signals in niches), key=lambda item: (-item[1], item[0]))[:max(1, limit)])
