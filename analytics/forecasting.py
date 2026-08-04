from __future__ import annotations

from math import sqrt
from statistics import fmean, pstdev


def moving_average_forecast(values: list[float], periods: int = 7, horizon: int = 7) -> list[float]:
    if horizon < 0:
        raise ValueError("horizon must be non-negative")
    if not values:
        return [0.0] * horizon
    window_size = max(1, int(periods))
    window = [float(value) for value in values[-window_size:]]
    forecast: list[float] = []
    for _ in range(horizon):
        value = sum(window[-window_size:]) / min(window_size, len(window))
        forecast.append(round(value, 4))
        window.append(value)
    return forecast


def linear_trend(values: list[float]) -> float:
    points = [float(value) for value in values]
    count = len(points)
    if count < 2:
        return 0.0
    mean_x = (count - 1) / 2
    mean_y = fmean(points)
    numerator = sum((index - mean_x) * (value - mean_y) for index, value in enumerate(points))
    denominator = sum((index - mean_x) ** 2 for index in range(count))
    return numerator / denominator if denominator else 0.0


def trend_adjusted_forecast(values: list[float], periods: int = 7, horizon: int = 7,
                            trend_weight: float = 0.35) -> list[float]:
    base = moving_average_forecast(values, periods, horizon)
    trend = linear_trend(values[-max(2, periods * 2):]) * max(0.0, min(1.0, trend_weight))
    return [round(max(0.0, value + trend * (index + 1)), 4) for index, value in enumerate(base)]


def prediction_interval(values: list[float], forecast: list[float], confidence_z: float = 1.96) -> tuple[list[float], list[float]]:
    history = [float(value) for value in values]
    spread = pstdev(history) if len(history) >= 2 else 0.0
    lower = [round(max(0.0, value - confidence_z * spread * sqrt(index + 1)), 4) for index, value in enumerate(forecast)]
    upper = [round(value + confidence_z * spread * sqrt(index + 1), 4) for index, value in enumerate(forecast)]
    return lower, upper
