from __future__ import annotations

from finance.reserve_calculator import ReserveCalculation, ReserveCalculator


class ChargebackReservePolicy:
    def evaluate(self,revenue_cad: object,chargeback_rate: object,*,average_loss_multiplier: object=1.15,minimum_cad: object=0) -> ReserveCalculation:
        multiplier=max(1.0,float(average_loss_multiplier))
        return ReserveCalculator().calculate("chargeback",revenue_cad,chargeback_rate,buffer_rate=multiplier-1,minimum_cad=minimum_cad,reason="historical_chargeback_rate")

def chargeback_reserve(revenue_cad: float,chargeback_rate: float,average_loss_multiplier: float=1.15) -> float:
    return float(ChargebackReservePolicy().evaluate(revenue_cad,chargeback_rate,average_loss_multiplier=average_loss_multiplier).reserve_cad)
