from __future__ import annotations


class ThresholdResolver:
    def __init__(self, defaults: dict[str, float] | None = None) -> None:
        self.defaults = {key: max(0.0, min(1.0, float(value))) for key, value in (defaults or {}).items()}

    def resolve(self, decision_type: str, *, risk: str = "normal", sample_size: int = 0) -> float:
        base = self.defaults.get(decision_type, 0.75)
        risk_adjustment = {"low": -0.05, "normal": 0.0, "high": 0.10, "critical": 0.20}.get(risk, 0.0)
        sample_adjustment = 0.05 if sample_size < 10 else (0.02 if sample_size < 50 else 0.0)
        return max(0.0, min(0.99, base + risk_adjustment + sample_adjustment))
