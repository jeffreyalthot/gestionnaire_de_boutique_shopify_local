from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DutyEstimate:
    customs_value: float
    duty: float
    tax: float
    brokerage: float
    total: float


class DutyEstimator:
    def estimate(self, customs_value: float, shipping: float, duty_rate: float, tax_rate: float, brokerage: float = 0.0) -> DutyEstimate:
        value=max(0.0,customs_value); freight=max(0.0,shipping)
        duty=value*max(0.0,duty_rate)
        tax=(value+freight+duty)*max(0.0,tax_rate)
        total=duty+tax+max(0.0,brokerage)
        return DutyEstimate(round(value,2),round(duty,2),round(tax,2),round(max(0.0,brokerage),2),round(total,2))
