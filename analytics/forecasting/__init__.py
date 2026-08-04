from __future__ import annotations


def moving_average_forecast(values: list[float], periods: int = 7, horizon: int = 7) -> list[float]:
    if not values:
        return [0.0] * horizon
    periods = max(1, periods)
    horizon = max(0, horizon)
    window = [float(value) for value in values[-periods:]]
    forecast: list[float] = []
    for _ in range(horizon):
        value = sum(window[-periods:]) / min(periods, len(window))
        forecast.append(round(value, 4))
        window.append(value)
    return forecast


__all__ = ["moving_average_forecast"]
