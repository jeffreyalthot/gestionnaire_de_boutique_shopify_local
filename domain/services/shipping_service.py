from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True)
class ShippingDecision:
    option: dict[str, object]
    score: float
    alternatives: int
    reason: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def choose_shipping_option(options: list[dict[str, object]]) -> dict[str, object]:
    return ShippingService().choose(options).option


class ShippingService:
    def choose(
        self,
        options: Iterable[dict[str, object]],
        *,
        maximum_days: int | None = None,
        require_tracking: bool = True,
        cost_weight: float = 0.6,
        speed_weight: float = 0.4,
    ) -> ShippingDecision:
        values = [dict(item) for item in options]
        if not values:
            raise ValueError("Aucune option d'expédition.")
        candidates = [item for item in values if not require_tracking or item.get("tracking", True)]
        if maximum_days is not None:
            candidates = [item for item in candidates if int(item.get("estimated_days", 999)) <= maximum_days]
        if not candidates:
            candidates = values
        max_cost = max(float(item.get("amount", 0) or 0) for item in candidates) or 1.0
        max_days = max(int(item.get("estimated_days", 999) or 999) for item in candidates) or 1
        ranked = []
        for item in candidates:
            cost = float(item.get("amount", 0) or 0)
            days = int(item.get("estimated_days", 999) or 999)
            reliability = max(0.0, min(1.0, float(item.get("reliability", 0.8) or 0.8)))
            score = (1 - cost / max_cost) * cost_weight + (1 - days / max_days) * speed_weight + reliability * 0.2
            ranked.append((score, cost, days, item))
        score, _, _, selected = max(ranked, key=lambda value: (value[0], -value[1], -value[2]))
        return ShippingDecision(selected, round(score, 6), len(candidates) - 1, "weighted_cost_speed_reliability")
