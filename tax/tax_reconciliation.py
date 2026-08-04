from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True, slots=True)
class TaxReconciliationResult:
    matched: bool
    collected_cad: Decimal
    expected_cad: Decimal
    drift_cad: Decimal
    drift_percent: Decimal
    severity: str
    action: str

    def as_dict(self) -> dict[str, object]:
        return {key: str(value) if isinstance(value, Decimal) else value for key, value in asdict(self).items()}


class TaxReconciliation:
    def compare(self, collected_cad: float, expected_cad: float, tolerance_cad: float = .05) -> dict[str, object]:
        result = self.reconcile(collected_cad, expected_cad, tolerance_cad=tolerance_cad)
        return {"matched": result.matched, "drift_cad": float(result.drift_cad)}

    def reconcile(self, collected_cad: object, expected_cad: object, *, tolerance_cad: object = .05, warning_percent: object = 1) -> TaxReconciliationResult:
        collected = Decimal(str(collected_cad)); expected = Decimal(str(expected_cad))
        drift = (collected - expected).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        percent = (abs(drift) / abs(expected) * 100).quantize(Decimal("0.01")) if expected else Decimal("0")
        matched = abs(drift) <= Decimal(str(tolerance_cad))
        severity = "none" if matched else "medium" if percent < Decimal(str(warning_percent)) else "high"
        action = "none" if matched else "review_rounding" if severity == "medium" else "open_tax_exception"
        return TaxReconciliationResult(matched, collected, expected, drift, percent, severity, action)
