from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExposureDecision:
    allowed: bool
    remaining_cad: float
    reason: str


class FinancialExposureGuard:
    def __init__(self, maximum_cad: float) -> None:
        self.maximum_cad = max(0.0, maximum_cad)

    def evaluate(self, current_cad: float, requested_cad: float) -> ExposureDecision:
        remaining = max(0.0, self.maximum_cad - current_cad)
        if requested_cad <= 0:
            return ExposureDecision(False, remaining, "invalid_amount")
        if requested_cad > remaining:
            return ExposureDecision(False, remaining, "exposure_limit")
        return ExposureDecision(True, remaining - requested_cad, "allowed")
