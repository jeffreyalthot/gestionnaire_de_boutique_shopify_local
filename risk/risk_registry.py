from __future__ import annotations

from collections.abc import Callable
from risk.risk_context import RiskContext
from risk.risk_score import RiskScore


class RiskRegistry:
    def __init__(self) -> None: self._assessors: dict[str,Callable[[RiskContext],RiskScore]]={}
    def register(self, name: str, assessor: Callable[[RiskContext],RiskScore]) -> None:
        if not name or name in self._assessors: raise ValueError("évaluateur invalide ou déjà enregistré")
        self._assessors[name]=assessor
    def assess(self, context: RiskContext) -> RiskScore:
        results=[fn(context) for fn in self._assessors.values()]
        if not results: return RiskScore.build(0)
        # Le risque le plus élevé domine; les raisons restent auditables.
        return RiskScore.build(max(x.score for x in results),[r for x in results for r in x.reasons])
    def names(self) -> tuple[str,...]: return tuple(sorted(self._assessors))
