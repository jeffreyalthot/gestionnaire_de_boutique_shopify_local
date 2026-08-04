from __future__ import annotations

from dataclasses import asdict, dataclass
from statistics import median
from typing import Any, Iterable


@dataclass(frozen=True, slots=True)
class AnomalyResult:
    anomalous: bool
    score: float
    center: float
    spread: float
    value: float
    reason: str
    severity: str = "none"
    direction: str = "stable"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class RobustAnomalyDetector:
    metric = "value"
    expected_direction = "both"

    def __init__(self, *, threshold: float = 3.5, minimum_samples: int = 7) -> None:
        self.threshold = max(1.0, threshold)
        self.minimum_samples = max(3, minimum_samples)

    def detect(self, history: Iterable[float], value: float) -> AnomalyResult:
        values = [float(item) for item in history]
        value = float(value)
        if len(values) < self.minimum_samples:
            return AnomalyResult(False, 0.0, median(values) if values else 0.0, 0.0, value, "insufficient_history")
        center = median(values)
        deviations = [abs(item - center) for item in values]
        mad = median(deviations)
        delta = value - center
        direction = "up" if delta > 0 else ("down" if delta < 0 else "stable")
        if mad <= 1e-12:
            score = 0.0 if abs(delta) <= 1e-12 else self.threshold + 1.0
        else:
            score = 0.6745 * abs(delta) / mad
        direction_allowed = self.expected_direction == "both" or direction == self.expected_direction
        anomalous = score >= self.threshold and direction_allowed
        severity = "critical" if score >= self.threshold * 2 else ("high" if anomalous else ("watch" if score >= self.threshold * .7 else "none"))
        return AnomalyResult(anomalous, round(score, 6), center, mad, value,
                             "robust_z_score" if anomalous else "within_range", severity, direction)

    def detect_series(self, values: Iterable[float]) -> tuple[AnomalyResult, ...]:
        history: list[float] = []
        results: list[AnomalyResult] = []
        for value in values:
            results.append(self.detect(history, float(value)))
            history.append(float(value))
        return tuple(results)
