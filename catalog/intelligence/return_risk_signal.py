from __future__ import annotations


def return_risk_signal(*, fragile: bool, sizing_complexity: float, defect_rate: float) -> float:
    return max(0.0, min(1.0, (0.25 if fragile else 0.0) + sizing_complexity * 0.35 + defect_rate * 4.0))
