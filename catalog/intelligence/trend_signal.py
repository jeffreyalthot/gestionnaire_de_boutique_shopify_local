from __future__ import annotations


def trend_signal(samples: list[float]) -> float:
    if len(samples) < 2:
        return 0.5
    first = sum(samples[: max(1, len(samples)//3)]) / max(1, len(samples)//3)
    last = sum(samples[-max(1, len(samples)//3):]) / max(1, len(samples)//3)
    if first <= 0:
        return 0.5
    growth = (last - first) / first
    return max(0.0, min(1.0, 0.5 + growth / 2))
