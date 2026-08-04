from __future__ import annotations


class ImageBackgroundPolicy:
    def evaluate(self, *, role: str, transparent: bool, background_uniformity: float) -> dict[str, object]:
        uniformity = max(0.0, min(1.0, background_uniformity))
        if role == "hero" and not transparent and uniformity < 0.75:
            return {"allowed": False, "reason": "hero_background_not_clean"}
        if role == "hero" and transparent:
            return {"allowed": True, "reason": "transparent_hero"}
        return {"allowed": True, "reason": "background_acceptable"}
