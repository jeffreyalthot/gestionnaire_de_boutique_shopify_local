from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ThresholdDecision:
    requires_review: bool
    amount_cad: float
    threshold_cad: float
    overage_cad: float
    reason: str
class ImportThresholds:
    def evaluate(self,declared_value_cad: float,threshold_cad: float,*,restricted: bool=False,commercial_quantity: bool=False) -> ThresholdDecision:
        amount=max(0.0,float(declared_value_cad));threshold=max(0.0,float(threshold_cad));over=max(0.0,amount-threshold);review=restricted or commercial_quantity or amount>threshold
        reason="restricted" if restricted else "commercial_quantity" if commercial_quantity else "threshold_exceeded" if amount>threshold else "within_threshold"
        return ThresholdDecision(review,round(amount,2),round(threshold,2),round(over,2),reason)
    def requires_review(self,declared_value_cad: float,threshold_cad: float) -> bool:return self.evaluate(declared_value_cad,threshold_cad).requires_review
