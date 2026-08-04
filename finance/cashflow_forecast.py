from __future__ import annotations

from analytics.forecasting import moving_average_forecast


class CashflowForecast:
    def forecast(self, inflows: list[float], outflows: list[float], *, horizon: int = 14) -> dict[str, list[float]]:
        incoming = moving_average_forecast(inflows, periods=min(7, max(1, len(inflows))), horizon=horizon)
        outgoing = moving_average_forecast(outflows, periods=min(7, max(1, len(outflows))), horizon=horizon)
        net = [round(i - o, 2) for i, o in zip(incoming, outgoing)]
        cumulative=[]; total=0.0
        for value in net:
            total += value; cumulative.append(round(total, 2))
        return {"inflow": incoming, "outflow": outgoing, "net": net, "cumulative": cumulative}
