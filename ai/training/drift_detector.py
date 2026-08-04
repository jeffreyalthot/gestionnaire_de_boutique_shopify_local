from __future__ import annotations

from collections import deque
from dataclasses import asdict, dataclass
from math import sqrt
from statistics import fmean, pstdev


@dataclass(frozen=True, slots=True)
class DriftReport:
    drifted: bool
    baseline_mean: float
    recent_mean: float
    absolute_shift: float
    standardized_shift: float
    samples: int

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class DriftDetector:
    """Bounded two-window error drift detector for online models."""

    def __init__(self, window: int = 100, threshold: float = 0.15, z_threshold: float = 2.5) -> None:
        if window < 10:
            raise ValueError("window must be at least 10")
        self.values: deque[float] = deque(maxlen=int(window))
        self.threshold = max(0.0, float(threshold))
        self.z_threshold = max(0.0, float(z_threshold))
        self.last_report = DriftReport(False, 0.0, 0.0, 0.0, 0.0, 0)

    def update(self, error: float) -> bool:
        self.values.append(float(error))
        self.last_report = self.report()
        return self.last_report.drifted

    def report(self) -> DriftReport:
        values = list(self.values)
        if len(values) < self.values.maxlen:
            return DriftReport(False, 0.0, 0.0, 0.0, 0.0, len(values))
        half = len(values) // 2
        baseline = values[:half]
        recent = values[half:]
        baseline_mean = fmean(baseline)
        recent_mean = fmean(recent)
        shift = recent_mean - baseline_mean
        pooled = sqrt((pstdev(baseline) ** 2 + pstdev(recent) ** 2) / 2) if len(values) > 2 else 0.0
        standardized = shift / pooled if pooled > 1e-12 else (float("inf") if shift > 0 else 0.0)
        drifted = shift > self.threshold and standardized >= self.z_threshold
        return DriftReport(
            drifted,
            round(baseline_mean, 8),
            round(recent_mean, 8),
            round(shift, 8),
            round(standardized, 8) if standardized != float("inf") else standardized,
            len(values),
        )

    def reset(self) -> None:
        self.values.clear()
        self.last_report = DriftReport(False, 0.0, 0.0, 0.0, 0.0, 0)
