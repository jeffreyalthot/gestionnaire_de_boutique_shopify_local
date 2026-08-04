from __future__ import annotations

from dataclasses import asdict, dataclass
from statistics import fmean
from typing import Any

from analytics.forecasting import linear_trend, prediction_interval, trend_adjusted_forecast


@dataclass(frozen=True, slots=True)
class ForecastResult:
    metric: str
    horizon: int
    values: tuple[float, ...]
    lower: tuple[float, ...]
    upper: tuple[float, ...]
    trend_per_period: float
    history_mean: float
    confidence: float

    def as_dict(self) -> dict[str, Any]:
        value = asdict(self)
        for key in ("values", "lower", "upper"):
            value[key] = list(value[key])
        return value


class MovingAverageForecaster:
    metric = "value"

    def __init__(self, *, confidence_z: float = 1.96, trend_weight: float = 0.35) -> None:
        self.confidence_z = max(0.0, float(confidence_z))
        self.trend_weight = max(0.0, min(1.0, float(trend_weight)))

    def forecast(self, values: list[float], *, periods: int = 7, horizon: int = 7) -> dict[str, object]:
        history = [float(value) for value in values]
        predicted = trend_adjusted_forecast(history, periods, horizon, self.trend_weight)
        lower, upper = prediction_interval(history, predicted, self.confidence_z)
        completeness = min(1.0, len(history) / max(1, periods * 3))
        result = ForecastResult(
            metric=self.metric,
            horizon=max(0, int(horizon)),
            values=tuple(predicted),
            lower=tuple(lower),
            upper=tuple(upper),
            trend_per_period=round(linear_trend(history), 6),
            history_mean=round(fmean(history), 6) if history else 0.0,
            confidence=round(completeness, 4),
        )
        return result.as_dict()
