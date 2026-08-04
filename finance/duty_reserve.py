from __future__ import annotations

from finance.reserve_calculator import ReserveCalculation, ReserveCalculator


class DutyReservePolicy:
    def evaluate(self,import_value_cad: object,estimated_duty_rate: object,*,uncertainty_buffer: object=.20,minimum_cad: object=0) -> ReserveCalculation:
        return ReserveCalculator().calculate("customs_duty",import_value_cad,estimated_duty_rate,buffer_rate=uncertainty_buffer,minimum_cad=minimum_cad,reason="landed_cost_uncertainty")

def duty_reserve(import_value_cad: float,estimated_duty_rate: float,uncertainty_buffer: float=.20) -> float:
    return float(DutyReservePolicy().evaluate(import_value_cad,estimated_duty_rate,uncertainty_buffer=uncertainty_buffer).reserve_cad)
