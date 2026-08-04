from __future__ import annotations

from analytics.forecasting_core import MovingAverageForecaster


class DemandForecast(MovingAverageForecaster):
    metric = "demand"

    def plan(self, values: list[float], *, periods: int = 7, horizon: int = 7) -> dict[str, object]:
        result = self.forecast(values, periods=periods, horizon=horizon)
        result["recommended_stock"] = round(sum(result["values"]), 4)
        return result
