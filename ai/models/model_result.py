from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from math import isfinite
from typing import Any, Iterable


@dataclass(frozen=True, slots=True)
class ModelResult:
    value: float
    confidence: float
    reasons: tuple[str, ...] = ()
    metadata: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        value = float(self.value)
        confidence = float(self.confidence)
        object.__setattr__(self, "value", value if isfinite(value) else 0.0)
        object.__setattr__(self, "confidence", max(0.0, min(1.0, confidence if isfinite(confidence) else 0.0)))
        object.__setattr__(self, "reasons", tuple(dict.fromkeys(str(item) for item in self.reasons if str(item))))
        object.__setattr__(self, "metadata", dict(self.metadata or {}))

    def bounded(self, lower: float = 0.0, upper: float = 1.0) -> "ModelResult":
        low, high = sorted((float(lower), float(upper)))
        return replace(self, value=max(low, min(high, self.value)))

    def with_reason(self, *reasons: str) -> "ModelResult":
        return replace(self, reasons=tuple(dict.fromkeys((*self.reasons, *reasons))))

    def with_metadata(self, **metadata: Any) -> "ModelResult":
        merged = dict(self.metadata or {})
        merged.update(metadata)
        return replace(self, metadata=merged)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def combine(cls, results: Iterable["ModelResult"], weights: Iterable[float] | None = None) -> "ModelResult":
        items = tuple(results)
        if not items:
            return cls(0.0, 0.0, ("no_results",), {})
        weight_values = tuple(float(value) for value in weights) if weights is not None else (1.0,) * len(items)
        if len(weight_values) != len(items):
            raise ValueError("weights_length_mismatch")
        positive = tuple(max(0.0, value) for value in weight_values)
        denominator = sum(positive) or float(len(items))
        if not sum(positive):
            positive = (1.0,) * len(items)
        value = sum(item.value * weight for item, weight in zip(items, positive, strict=True)) / denominator
        confidence = sum(item.confidence * weight for item, weight in zip(items, positive, strict=True)) / denominator
        reasons = tuple(dict.fromkeys(reason for item in items for reason in item.reasons))
        return cls(value, confidence, reasons, {"components": len(items)})
