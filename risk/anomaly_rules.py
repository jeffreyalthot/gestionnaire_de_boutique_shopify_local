from __future__ import annotations


def detect_anomalies(values: list[float], *, z_limit: float = 3.5) -> list[int]:
    if len(values) < 5:
        return []
    ordered = sorted(values)
    median = ordered[len(ordered)//2]
    deviations = sorted(abs(value - median) for value in values)
    mad = deviations[len(deviations)//2] or 1e-9
    return [index for index, value in enumerate(values) if abs(0.6745 * (value - median) / mad) > z_limit]
