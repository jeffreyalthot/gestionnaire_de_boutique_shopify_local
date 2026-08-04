from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DimensionDecision:
    allowed: bool
    reason: str


def validate_dimensions(width: int, height: int, *, minimum: int = 400, maximum: int = 10000, maximum_pixels: int = 36_000_000) -> DimensionDecision:
    if width < minimum or height < minimum:
        return DimensionDecision(False, "too_small")
    if width > maximum or height > maximum or width * height > maximum_pixels:
        return DimensionDecision(False, "too_large")
    ratio = max(width / height, height / width)
    if ratio > 4.0:
        return DimensionDecision(False, "extreme_aspect_ratio")
    return DimensionDecision(True, "allowed")
