from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from catalog.discovery.product_candidate import ProductCandidate


@dataclass(frozen=True, slots=True)
class RankedProduct:
    candidate: ProductCandidate
    score: float
    reasons: tuple[str, ...]


class ProductRanker:
    WEIGHTS = {"demand": 0.24, "margin": 0.24, "supplier": 0.18, "quality": 0.14, "shipping": 0.10, "competition": -0.06, "return_risk": -0.04}

    def score(self, candidate: ProductCandidate) -> RankedProduct:
        total = 0.0
        reasons: list[str] = []
        for name, weight in self.WEIGHTS.items():
            value = max(0.0, min(1.0, float(candidate.signals.get(name, 0.5))))
            contribution = value * weight if weight >= 0 else (1 - value) * abs(weight)
            total += contribution
            reasons.append(f"{name}:{value:.2f}")
        return RankedProduct(candidate, round(max(0.0, min(1.0, total)), 4), tuple(reasons))

    def rank(self, candidates: Iterable[ProductCandidate], limit: int = 50) -> list[RankedProduct]:
        return sorted((self.score(item) for item in candidates), key=lambda item: item.score, reverse=True)[:limit]
