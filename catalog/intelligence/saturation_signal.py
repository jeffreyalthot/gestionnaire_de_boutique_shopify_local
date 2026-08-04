from __future__ import annotations

import math


def saturation_signal(*, competing_listings: int, dominant_brand_share: float,
                      price_dispersion: float) -> float:
    listings = math.log1p(max(0, competing_listings)) / math.log1p(10000)
    dominance = max(0.0, min(1.0, dominant_brand_share))
    dispersion_penalty = max(0.0, min(1.0, 1.0 - price_dispersion))
    return round(max(0.0, min(1.0, 0.50 * listings + 0.35 * dominance + 0.15 * dispersion_penalty)), 6)
