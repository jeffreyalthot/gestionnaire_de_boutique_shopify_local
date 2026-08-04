from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ImageQuality:
    score: float
    accepted: bool
    issues: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class ImageQualityAnalyzer:
    def analyze(self, *, width: int, height: int, byte_size: int, content_type: str,
                duplicate: bool = False, watermark_detected: bool = False) -> ImageQuality:
        issues: list[str] = []
        score = 1.0
        if min(width, height) < 800:
            issues.append("low_resolution"); score -= 0.25
        if max(width, height) > 10000:
            issues.append("excessive_resolution"); score -= 0.10
        if byte_size > 12 * 1024 * 1024:
            issues.append("file_too_large"); score -= 0.15
        if content_type not in {"image/jpeg", "image/png", "image/webp", "image/gif"}:
            issues.append("unsupported_type"); score -= 0.50
        if duplicate:
            issues.append("duplicate"); score -= 0.20
        if watermark_detected:
            issues.append("watermark"); score -= 0.30
        score = max(0.0, min(1.0, score))
        return ImageQuality(round(score, 6), score >= 0.70 and not watermark_detected, tuple(issues))
