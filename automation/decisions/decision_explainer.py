from __future__ import annotations

from typing import Any


class DecisionExplainer:
    def explain(self, *, score: float, threshold: float, contributions: dict[str, float], rules: tuple[dict[str, str], ...] = ()) -> dict[str, Any]:
        ordered = sorted(contributions.items(), key=lambda item: (-abs(item[1]), item[0]))
        drivers = tuple({"feature": key, "contribution": round(value, 6)} for key, value in ordered[:5])
        blockers = tuple(rule for rule in rules if rule.get("effect") in {"deny", "hold"})
        return {
            "decision": "accept" if score >= threshold and not blockers else "hold",
            "score": round(score, 6),
            "threshold": round(threshold, 6),
            "margin": round(score - threshold, 6),
            "drivers": drivers,
            "blockers": blockers,
        }
