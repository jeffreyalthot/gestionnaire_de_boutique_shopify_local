from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class QualityDecision:
    passed: bool
    score: float
    failures: tuple[str, ...]


class QualityGate:
    def evaluate(self, checks: dict[str, float], thresholds: dict[str, float] | None = None) -> QualityDecision:
        thresholds = thresholds or {name: 0.7 for name in checks}
        failures = tuple(name for name, value in checks.items() if float(value) < float(thresholds.get(name, 0.7)))
        score = sum(max(0.0, min(1.0, float(value))) for value in checks.values()) / max(1, len(checks))
        return QualityDecision(not failures, round(score, 4), failures)
