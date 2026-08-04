from __future__ import annotations

from collections import defaultdict
from typing import Iterable


class ChannelAttribution:
    def allocate(self, touchpoints: Iterable[dict[str, object]], revenue: float, *, model: str = "linear") -> dict[str, float]:
        points = list(touchpoints)
        if not points or revenue <= 0:
            return {}
        if model not in {"first_touch", "last_touch", "linear", "position_based"}:
            raise ValueError("Modèle d'attribution invalide.")
        weights = [0.0] * len(points)
        if model == "first_touch":
            weights[0] = 1.0
        elif model == "last_touch":
            weights[-1] = 1.0
        elif model == "linear":
            weights = [1.0 / len(points)] * len(points)
        elif len(points) == 1:
            weights[0] = 1.0
        elif len(points) == 2:
            weights = [0.5, 0.5]
        else:
            weights[0] = weights[-1] = 0.4
            middle = 0.2 / (len(points) - 2)
            for index in range(1, len(points) - 1):
                weights[index] = middle
        output: dict[str, float] = defaultdict(float)
        for point, weight in zip(points, weights):
            output[str(point.get("channel", "unknown"))] += revenue * weight
        return {key: round(value, 2) for key, value in sorted(output.items())}
