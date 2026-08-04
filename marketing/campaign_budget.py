from __future__ import annotations


def allocate_budget(total_cad: float, channels: dict[str, float], minimum_cad: float = 0.0) -> dict[str, float]:
    if total_cad < 0:
        raise ValueError("Budget négatif")
    positive = {name: max(0.0, weight) for name, weight in channels.items()}
    total_weight = sum(positive.values()) or 1.0
    result = {name: round(max(minimum_cad, total_cad * weight / total_weight), 2) for name, weight in positive.items()}
    allocated = sum(result.values())
    if allocated > total_cad and allocated > 0:
        scale = total_cad / allocated
        result = {name: round(value * scale, 2) for name, value in result.items()}
    return result
