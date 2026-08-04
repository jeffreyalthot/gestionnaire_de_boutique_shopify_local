from __future__ import annotations
from ai.models.model_result import ModelResult

def _b(v: object) -> float:
    try:return max(0.0,min(1.0,float(v)))
    except (TypeError,ValueError):return 0.0

def assess_supplier_risk(dispute_rate: float,response_rate: float,years: float,verified: bool,
                         late_rate: float=0.0,quality_score: float=1.0,trade_assurance: bool=True) -> ModelResult:
    components={
        "disputes": _b(dispute_rate*5), "response": 1-_b(response_rate),
        "tenure": 1-_b(years/10), "verification": 0.0 if verified else 1.0,
        "late": _b(late_rate*2), "quality": 1-_b(quality_score),
        "assurance": 0.0 if trade_assurance else 1.0,
    }
    weights={"disputes":.24,"response":.15,"tenure":.08,"verification":.14,"late":.14,"quality":.15,"assurance":.10}
    risk=sum(components[k]*weights[k] for k in weights)
    reasons=tuple(k for k,v in components.items() if v>=.5)
    confidence=.95 if verified and years>=1 else .75
    return ModelResult(round(_b(risk),6),confidence,reasons,components)

def supplier_risk(dispute_rate: float,response_rate: float,years: float,verified: bool) -> float:
    return assess_supplier_risk(dispute_rate,response_rate,years,verified).value
