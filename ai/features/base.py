from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from math import isfinite
from typing import Mapping


def as_float(value: object, default: float = 0.0) -> float:
    """Convertit une valeur externe en flottant fini sans propager d'exception."""
    try:
        result = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError, OverflowError):
        return default
    return result if isfinite(result) else default


def bounded(value: object, minimum: float = 0.0, maximum: float = 1.0) -> float:
    if maximum < minimum:
        raise ValueError("maximum doit être supérieur ou égal à minimum")
    return min(maximum, max(minimum, as_float(value, minimum)))


def safe_ratio(numerator: object, denominator: object, default: float = 0.0) -> float:
    den = as_float(denominator)
    if den == 0.0:
        return default
    return as_float(numerator) / den


def age_hours(value: object, *, now: datetime | None = None, default: float = 0.0) -> float:
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, str) and value.strip():
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return default
    else:
        return default
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    reference = now or datetime.now(timezone.utc)
    return max(0.0, (reference - parsed.astimezone(timezone.utc)).total_seconds() / 3600.0)


@dataclass(frozen=True, slots=True)
class FeatureVector:
    values: Mapping[str, float]

    def normalized(self) -> dict[str, float]:
        return {str(key): as_float(value) for key, value in sorted(self.values.items())}

    def with_prefix(self, prefix: str) -> dict[str, float]:
        clean = prefix.strip().rstrip(".")
        return {f"{clean}.{key}" if clean else key: value for key, value in self.normalized().items()}
