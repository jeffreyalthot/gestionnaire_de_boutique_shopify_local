from __future__ import annotations

from analytics.forecasting_core import MovingAverageForecaster


class RevenueForecast(MovingAverageForecaster):
    metric = "revenue"

    def plan(self, values: list[float], *, periods: int = 7, horizon: int = 7) -> dict[str, object]:
        result = self.forecast(values, periods=periods, horizon=horizon)
        result["projected_revenue"] = round(sum(result["values"]), 4)
        return result
