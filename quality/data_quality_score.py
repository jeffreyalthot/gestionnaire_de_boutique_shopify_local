from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class QualityDimension:
    name: str
    score: float
    weight: float
    contribution: float


@dataclass(frozen=True, slots=True)
class QualityScoreResult:
    score: float
    grade: str
    dimensions: tuple[QualityDimension, ...]
    warnings: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class DataQualityScore:
    def combine(self, scores: list[float], weights: list[float] | None = None) -> float:
        return self.evaluate({str(index): score for index, score in enumerate(scores)}, dict(zip(map(str, range(len(scores))), weights or [1.] * len(scores)))).score

    def evaluate(self, scores: dict[str, float], weights: dict[str, float] | None = None) -> QualityScoreResult:
        if not scores:
            return QualityScoreResult(0.0, "F", (), ("no_dimensions",))
        weights = weights or {name: 1.0 for name in scores}
        dimensions: list[QualityDimension] = []
        total_weight = sum(max(0.0, float(weights.get(name, 1))) for name in scores) or 1.0
        warnings: list[str] = []
        for name, raw in scores.items():
            score = max(0.0, min(1.0, float(raw))); weight = max(0.0, float(weights.get(name, 1)))
            contribution = score * weight / total_weight
            dimensions.append(QualityDimension(name, round(score, 4), weight, round(contribution, 4)))
            if score < .5:
                warnings.append(f"low:{name}")
        total = round(sum(item.contribution for item in dimensions), 4)
        grade = "A" if total >= .9 else "B" if total >= .8 else "C" if total >= .7 else "D" if total >= .6 else "F"
        return QualityScoreResult(total, grade, tuple(dimensions), tuple(warnings))
