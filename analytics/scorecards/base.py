from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Scorecard:
    name: str
    score: float
    grade: str
    metrics: dict[str, float]
    issues: tuple[str, ...]
    recommendations: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class ScorecardBuilder:
    name = "generic"
    weights: dict[str, float] = {}
    minimums: dict[str, float] = {}

    def build(self, metrics: dict[str, float], issues: tuple[str, ...] = ()) -> Scorecard:
        normalized = {str(key): max(0.0, min(1.0, float(value))) for key, value in metrics.items()}
        if self.weights:
            denominator = sum(abs(value) for value in self.weights.values()) or 1.0
            score = sum(normalized.get(key, 0.0) * weight for key, weight in self.weights.items()) / denominator
        else:
            score = sum(normalized.values()) / max(1, len(normalized))
        threshold_issues = tuple(
            f"{key}_below_minimum" for key, minimum in self.minimums.items()
            if normalized.get(key, 0.0) < minimum
        )
        all_issues = tuple(dict.fromkeys((*issues, *threshold_issues)))
        score = max(0.0, min(1.0, score - min(0.30, 0.03 * len(all_issues))))
        grade = "A" if score >= 0.90 else ("B" if score >= 0.80 else ("C" if score >= 0.70 else ("D" if score >= 0.60 else "F")))
        recommendations = tuple(self.recommendation(issue) for issue in all_issues)
        return Scorecard(self.name, round(score, 6), grade, normalized, all_issues, recommendations)

    def compare(self, current: dict[str, float], previous: dict[str, float]) -> dict[str, float]:
        keys = set(current) | set(previous)
        return {key: round(float(current.get(key, 0.0)) - float(previous.get(key, 0.0)), 6) for key in sorted(keys)}

    @staticmethod
    def recommendation(issue: str) -> str:
        return f"review:{issue}"
