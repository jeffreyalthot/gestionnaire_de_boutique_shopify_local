from __future__ import annotations
import math
from ai.models.model_result import ModelResult
from ai.models.online_regressor import OnlineRegressor

class ReturnProbabilityModel(OnlineRegressor):
    def probability(self,features: list[float]) -> float:return max(0.0,min(1.0,self.predict(features,0.05)))
    def assess(self,*,category_rate: float,customer_rate: float,size_risk: float,delivery_risk: float,description_gap: float=0.0) -> ModelResult:
        signals=[category_rate,customer_rate,size_risk,delivery_risk,description_gap]
        weights=[.28,.22,.18,.18,.14]
        linear=sum(max(0.0,min(1.0,float(v)))*w for v,w in zip(signals,weights,strict=True))
        probability=1/(1+math.exp(-6*(linear-.5)))
        confidence=.65+.07*sum(v is not None for v in signals)
        return ModelResult(round(probability,6),min(1.0,confidence),("category","customer","delivery"),{"linear":linear})
