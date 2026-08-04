from __future__ import annotations
from ai.models.model_result import ModelResult
from ai.models.online_classifier import OnlineTextClassifier

class ConversionPredictor(OnlineTextClassifier):
    def __init__(self) -> None:super().__init__(["low","high"])
    def assess(self,*,views: int,add_to_carts: int,checkouts: int,orders: int,benchmark_rate: float=.02) -> ModelResult:
        views=max(0,int(views)); orders=max(0,int(orders)); carts=max(0,int(add_to_carts)); checkouts=max(0,int(checkouts))
        rate=orders/max(1,views); funnel=(carts/max(1,views)+checkouts/max(1,carts)+orders/max(1,checkouts))/3
        score=max(0.0,min(1.0,.6*(rate/max(.0001,benchmark_rate))+.4*funnel))
        confidence=min(1.0,views/500)
        return ModelResult(round(score,6),round(confidence,6),("observed_funnel",),{"conversion_rate":rate,"funnel":funnel})
