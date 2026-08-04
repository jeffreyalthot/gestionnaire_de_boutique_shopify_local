from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class RiskScore:
    score: float
    level: str
    reasons: tuple[str, ...] = ()
    factors: tuple[tuple[str, float], ...] = ()
    recommended_action: str = "allow"
    confidence: float = 1.0

    @classmethod
    def build(cls, score: float, reasons=(), *, factors: dict[str, float] | None = None, confidence: float = 1.0) -> "RiskScore":
        value = max(0.0, min(1.0, float(score)))
        level = "low" if value < .25 else "medium" if value < .5 else "high" if value < .75 else "critical"
        action = "allow" if level == "low" else "review" if level == "medium" else "hold" if level == "high" else "block"
        ranked = tuple(sorted(((str(k), round(float(v), 4)) for k, v in (factors or {}).items() if v), key=lambda item: abs(item[1]), reverse=True))
        return cls(round(value, 4), level, tuple(dict.fromkeys(map(str, reasons))), ranked, action, round(max(0.0, min(1.0, confidence)), 4))

    def combine(self, other: "RiskScore", *, weight: float = .5) -> "RiskScore":
        w = max(0.0, min(1.0, float(weight)))
        score = self.score * (1 - w) + other.score * w
        factors = dict(self.factors)
        for key, value in other.factors:
            factors[key] = factors.get(key, 0.0) + value * w
        return self.build(score, (*self.reasons, *other.reasons), factors=factors, confidence=min(self.confidence, other.confidence))

    def as_dict(self) -> dict[str, object]:
        return asdict(self)
