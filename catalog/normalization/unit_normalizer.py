from __future__ import annotations

CONVERSIONS = {("kg", "g"): 1000.0, ("g", "kg"): .001, ("lb", "kg"): .45359237, ("oz", "g"): 28.349523125, ("cm", "mm"): 10.0, ("in", "cm"): 2.54}


def normalize_unit(value: float, source: str, target: str) -> float:
    source=source.lower(); target=target.lower()
    if source == target: return float(value)
    key=(source,target)
    if key not in CONVERSIONS: raise ValueError(f"Conversion non supportée: {source}->{target}")
    return float(value)*CONVERSIONS[key]
