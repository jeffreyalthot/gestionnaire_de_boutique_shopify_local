from __future__ import annotations


class WeightNormalizer:
    FACTORS = {"mg": 0.000001, "g": 0.001, "kg": 1.0, "oz": 0.028349523125, "lb": 0.45359237}

    def normalize_kg(self, value: float, unit: str) -> float:
        factor = self.FACTORS.get(unit.casefold())
        if factor is None:
            raise ValueError("Unité de poids non supportée.")
        result = max(0.0, float(value) * factor)
        if result > 10000:
            raise ValueError("Poids irréaliste.")
        return round(result, 6)
