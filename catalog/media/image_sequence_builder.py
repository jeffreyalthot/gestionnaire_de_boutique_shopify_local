from __future__ import annotations

from typing import Iterable


class ImageSequenceBuilder:
    ROLE_ORDER = {"hero": 0, "angle": 1, "detail": 2, "scale": 3, "lifestyle": 4, "packaging": 5}

    def build(self, images: Iterable[dict[str, object]], maximum: int = 12) -> tuple[dict[str, object], ...]:
        unique: dict[str, dict[str, object]] = {}
        for image in images:
            digest = str(image.get("sha256", image.get("url", "")))
            if digest and digest not in unique:
                unique[digest] = dict(image)
        ordered = sorted(unique.values(), key=lambda image: (
            self.ROLE_ORDER.get(str(image.get("role", "angle")), 99),
            -float(image.get("quality_score", 0.0) or 0.0),
            str(image.get("url", "")),
        ))
        return tuple(ordered[:max(1, min(maximum, 20))])
