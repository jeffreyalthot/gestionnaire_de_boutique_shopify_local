from __future__ import annotations

from collections import deque
from dataclasses import asdict, dataclass
from math import isfinite, sqrt
from statistics import fmean, median
from typing import Any, Iterable


@dataclass(frozen=True, slots=True)
class AnomalyAssessment:
    anomalous: bool
    score: float
    threshold: float
    center: tuple[float, ...]
    scale: tuple[float, ...]
    observations: int
    reasons: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class OnlineAnomalyDetector:
    """Détecteur robuste en flux, sans dépendance NumPy/scikit-learn obligatoire."""

    def __init__(self, *, threshold: float = 4.0, window: int = 256, minimum_samples: int = 8) -> None:
        self.threshold = max(1.0, float(threshold))
        self.minimum_samples = max(3, int(minimum_samples))
        self._rows: deque[tuple[float, ...]] = deque(maxlen=max(self.minimum_samples, int(window)))
        self.dimensions = 0
        self.fitted = False

    @staticmethod
    def _row(row: Iterable[float]) -> tuple[float, ...]:
        values = tuple(float(value) for value in row)
        if not values or any(not isfinite(value) for value in values):
            raise ValueError("anomaly_row_invalid")
        return values

    def partial_fit(self, rows: list[list[float]]) -> None:
        for raw in rows:
            row = self._row(raw)
            if self.dimensions and len(row) != self.dimensions:
                raise ValueError("anomaly_dimension_mismatch")
            self.dimensions = len(row)
            self._rows.append(row)
        self.fitted = len(self._rows) >= self.minimum_samples

    def _center_scale(self) -> tuple[tuple[float, ...], tuple[float, ...]]:
        if not self._rows:
            return (), ()
        columns = tuple(tuple(row[index] for row in self._rows) for index in range(self.dimensions))
        centers = tuple(median(column) for column in columns)
        scales = []
        for column, center in zip(columns, centers, strict=True):
            deviations = tuple(abs(value - center) for value in column)
            mad = median(deviations)
            if mad <= 1e-12:
                variance = fmean((value - center) ** 2 for value in column)
                mad = sqrt(variance) if variance > 1e-12 else 1.0
            scales.append(mad)
        return centers, tuple(scales)

    def assess(self, row: list[float]) -> AnomalyAssessment:
        values = self._row(row)
        if self.dimensions and len(values) != self.dimensions:
            raise ValueError("anomaly_dimension_mismatch")
        if not self.fitted:
            return AnomalyAssessment(False, 0.0, self.threshold, (), (), len(self._rows), ("insufficient_history",))
        centers, scales = self._center_scale()
        dimension_scores = tuple(0.6745 * abs(value - center) / max(scale, 1e-12) for value, center, scale in zip(values, centers, scales, strict=True))
        score = sqrt(sum(item * item for item in dimension_scores) / len(dimension_scores))
        reasons = tuple(f"dimension:{index}" for index, item in enumerate(dimension_scores) if item >= self.threshold)
        return AnomalyAssessment(score >= self.threshold, round(score, 6), self.threshold, centers, scales, len(self._rows), reasons or ("within_range",))

    def is_anomaly(self, row: list[float]) -> bool:
        return self.assess(row).anomalous

    def update_and_assess(self, row: list[float]) -> AnomalyAssessment:
        assessment = self.assess(row)
        if not assessment.anomalous:
            self.partial_fit([row])
        return assessment

    def statistics(self) -> dict[str, Any]:
        return {"observations": len(self._rows), "dimensions": self.dimensions, "fitted": self.fitted, "threshold": self.threshold}
