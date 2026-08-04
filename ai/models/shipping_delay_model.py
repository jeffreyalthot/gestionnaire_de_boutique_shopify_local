from __future__ import annotations
from ai.models.model_result import ModelResult
from ai.models.online_regressor import OnlineRegressor

class ShippingDelayModel(OnlineRegressor):
    def expected_days(self,features: list[float]) -> float:return max(0.0,self.predict(features,14))
    def estimate(self,*,quoted_days: float,carrier_late_rate: float,supplier_late_rate: float,customs_risk: float,seasonal_pressure: float=0.0) -> ModelResult:
        base=max(0.0,float(quoted_days)); risk=.35*carrier_late_rate+.30*supplier_late_rate+.20*customs_risk+.15*seasonal_pressure
        delay=max(0.0,base*(1+max(0.0,min(1.0,risk))))
        return ModelResult(round(delay,2),round(max(.3,1-risk*.6),4),tuple(k for k,v in {"carrier":carrier_late_rate,"supplier":supplier_late_rate,"customs":customs_risk,"seasonal":seasonal_pressure}.items() if v>=.4))
