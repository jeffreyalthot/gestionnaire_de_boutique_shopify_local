from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class DecisionScore:
    score: float
    confidence: float
    accepted: bool
    reasons: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class DecisionEngine:
    def score(self, signals: Mapping[str, float], weights: Mapping[str, float], *, threshold: float = 0.65) -> DecisionScore:
        common = sorted(set(signals) & set(weights))
        if not common:
            return DecisionScore(0.0, 0.0, False, ("no_signals",))
        total_weight = sum(abs(float(weights[name])) for name in common) or 1.0
        weighted = sum(max(0.0, min(1.0, float(signals[name]))) * float(weights[name]) for name in common)
        score = max(0.0, min(1.0, weighted / total_weight))
        confidence = min(1.0, len(common) / max(3.0, len(weights)))
        reasons = tuple(f"{name}={signals[name]:.3f}" for name in common)
        return DecisionScore(score, confidence, score >= threshold, reasons)
