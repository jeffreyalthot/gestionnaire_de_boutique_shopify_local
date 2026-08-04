from __future__ import annotations
from statistics import fmean, pstdev
from ai.models.model_result import ModelResult
from ai.models.online_regressor import OnlineRegressor

class DemandForecaster(OnlineRegressor):
    def features(self,views: float,orders: float,stock: float,price: float) -> list[float]:
        return [max(0.0,float(views)),max(0.0,float(orders)),max(0.0,float(stock)),max(0.0,float(price))]
    def forecast(self,history: list[float], horizon_days: int=7, trend_weight: float=.6) -> ModelResult:
        values=[max(0.0,float(v)) for v in history[-90:]]
        if not values:return ModelResult(0.0,0.0,("missing_history",),{"horizon_days":horizon_days})
        short=values[-min(7,len(values)):]; long=values[-min(28,len(values)):]
        recent=fmean(short); baseline=fmean(long)
        trend=(recent-baseline)*max(0.0,min(1.0,trend_weight))
        daily=max(0.0,recent+trend)
        variation=pstdev(long) if len(long)>1 else 0.0
        confidence=max(.1,min(1.0,len(values)/28))*max(.2,1-min(1.0,variation/max(1.0,baseline)))
        return ModelResult(round(daily*max(1,horizon_days),4),round(confidence,4),("moving_average","trend_adjusted"),{"daily":daily,"variation":variation})
