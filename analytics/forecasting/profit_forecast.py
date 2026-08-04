from __future__ import annotations

from analytics.forecasting_core import MovingAverageForecaster


class ProfitForecast(MovingAverageForecaster):
    metric = "profit"

    def plan(self, values: list[float], *, periods: int = 7, horizon: int = 7) -> dict[str, object]:
        result = self.forecast(values, periods=periods, horizon=horizon)
        result["projected_profit"] = round(sum(result["values"]), 4)
        return result
