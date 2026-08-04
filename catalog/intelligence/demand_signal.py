from __future__ import annotations

import math


def demand_signal(*, search_volume: float, order_velocity: float, review_velocity: float,
                  seasonality: float = 1.0) -> float:
    volume = math.log1p(max(0.0, search_volume)) / math.log1p(100000.0)
    orders = math.log1p(max(0.0, order_velocity)) / math.log1p(1000.0)
    reviews = math.log1p(max(0.0, review_velocity)) / math.log1p(500.0)
    score = (0.45 * volume + 0.40 * orders + 0.15 * reviews) * max(0.5, min(1.5, seasonality))
    return round(max(0.0, min(1.0, score)), 6)
