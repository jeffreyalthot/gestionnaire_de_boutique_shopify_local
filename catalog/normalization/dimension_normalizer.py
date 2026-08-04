from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class NormalizedDimensions:
    length_cm: float
    width_cm: float
    height_cm: float

    def as_dict(self):
        return asdict(self)


class DimensionNormalizer:
    FACTORS = {"mm": 0.1, "cm": 1.0, "m": 100.0, "in": 2.54, "inch": 2.54, "ft": 30.48}

    def normalize(self, length: float, width: float, height: float, unit: str) -> NormalizedDimensions:
        factor = self.FACTORS.get(unit.casefold())
        if factor is None:
            raise ValueError("Unité de dimension non supportée.")
        values = [max(0.0, float(value) * factor) for value in (length, width, height)]
        if any(value > 100000 for value in values):
            raise ValueError("Dimension irréaliste.")
        return NormalizedDimensions(*(round(value, 3) for value in values))
