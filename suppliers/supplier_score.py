from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class SupplierScore:
    supplier_id: str
    score: float
    risk_level: str
    metrics: dict[str, float]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class SupplierScorer:
    WEIGHTS = {"on_time": 0.25, "quality": 0.25, "response": 0.12, "trade_assurance": 0.12, "years": 0.08, "refund_resolution": 0.10, "inventory_accuracy": 0.08}

    def score(self, supplier_id: str, metrics: Mapping[str, float]) -> SupplierScore:
        normalized = {name: max(0.0, min(1.0, float(metrics.get(name, 0.5)))) for name in self.WEIGHTS}
        score = sum(normalized[name] * weight for name, weight in self.WEIGHTS.items())
        risk = "low" if score >= 0.82 else "medium" if score >= 0.65 else "high" if score >= 0.45 else "critical"
        return SupplierScore(supplier_id, round(score, 4), risk, normalized)
