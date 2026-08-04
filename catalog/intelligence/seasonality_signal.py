from __future__ import annotations

from math import cos, pi


def seasonality_signal(target_month: int, peak_month: int, spread_months: float = 2.5) -> float:
    distance = min((target_month - peak_month) % 12, (peak_month - target_month) % 12)
    if spread_months <= 0:
        return 1.0 if distance == 0 else 0.0
    return max(0.0, (cos(min(pi, distance / spread_months * pi)) + 1) / 2)
