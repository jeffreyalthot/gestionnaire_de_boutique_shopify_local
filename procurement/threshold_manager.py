from dataclasses import dataclass
from datetime import datetime,timezone
@dataclass(frozen=True,slots=True)
class ThresholdDecision:
    ready: bool
    reason: str
class ThresholdManager:
    def __init__(self,threshold_cad: float,max_age_minutes: int,max_orders: int) -> None:
        self.threshold=threshold_cad; self.max_age=max_age_minutes; self.max_orders=max_orders
    def evaluate(self,total_cad: float,created_at: str,order_count: int,urgent: bool=False) -> ThresholdDecision:
        age=(datetime.now(timezone.utc)-datetime.fromisoformat(created_at)).total_seconds()/60
        if urgent: return ThresholdDecision(True,"Commande urgente.")
        if total_cad>=self.threshold: return ThresholdDecision(True,"Seuil monétaire atteint.")
        if age>=self.max_age: return ThresholdDecision(True,"Âge maximal atteint.")
        if order_count>=self.max_orders: return ThresholdDecision(True,"Nombre maximal de commandes atteint.")
        return ThresholdDecision(False,"Lot en accumulation.")
