from __future__ import annotations
from ai.models.model_result import ModelResult

DEFAULT_WEIGHTS = {"quality": .22, "supplier": .18, "margin": .20, "stock": .12,
                   "delivery": .10, "demand": .12, "compliance": .06}

def _bounded(value: object) -> float:
    try: number=float(value)
    except (TypeError,ValueError): return 0.0
    return max(0.0,min(1.0,number))

def rank_product(features: dict[str,float], weights: dict[str,float] | None=None) -> ModelResult:
    weights=dict(weights or DEFAULT_WEIGHTS)
    total=sum(max(0.0,float(w)) for w in weights.values()) or 1.0
    weighted=sum(_bounded(features.get(name,0.0))*max(0.0,float(weight)) for name,weight in weights.items())/total
    penalties=.18*_bounded(features.get("return_risk",0))+ .25*_bounded(features.get("restriction_risk",0)) + .12*_bounded(features.get("saturation",0))
    missing=tuple(name for name in weights if name not in features)
    confidence=max(0.0,1.0-len(missing)/max(1,len(weights)))
    value=max(0.0,min(1.0,weighted-penalties))
    reasons=tuple(f"missing:{x}" for x in missing)
    return ModelResult(round(value,6),round(confidence,6),reasons,{"weighted":weighted,"penalties":penalties})

def product_rank(features: dict[str,float]) -> float:
    return rank_product(features).value
