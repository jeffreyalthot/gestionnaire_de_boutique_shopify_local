from __future__ import annotations

from analytics.forecasting_core import MovingAverageForecaster


class InventoryForecast(MovingAverageForecaster):
    metric = "inventory"

    def plan(self, values: list[float], *, periods: int = 7, horizon: int = 7) -> dict[str, object]:
        result = self.forecast(values, periods=periods, horizon=horizon)
        result["projected_minimum"] = round(min(result["values"], default=0.0), 4)
        return result
