from __future__ import annotations
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class SegmentTargetDecision:
    eligible: bool
    matched: tuple[str,...]
    missing: tuple[str,...]
    excluded: tuple[str,...]
    score: float
    reason: str
    def as_dict(self):return asdict(self)

class CustomerSegmentTargeting:
    def eligible(self,customer_segments: set[str],required: set[str],excluded: set[str]|None=None) -> bool:return self.evaluate(customer_segments,required,excluded).eligible
    def evaluate(self,customer_segments: set[str],required: set[str],excluded: set[str]|None=None,*,minimum_match_ratio: float=1.0) -> SegmentTargetDecision:
        values={str(v).strip().lower() for v in customer_segments};req={str(v).strip().lower() for v in required};blocked={str(v).strip().lower() for v in (excluded or set())}
        matched=req&values;missing=req-values;excluded_hits=blocked&values;ratio=len(matched)/len(req) if req else 1.0;eligible=ratio>=max(0,min(1,minimum_match_ratio)) and not excluded_hits
        reason="eligible" if eligible else "excluded_segment" if excluded_hits else "missing_required_segments"
        return SegmentTargetDecision(eligible,tuple(sorted(matched)),tuple(sorted(missing)),tuple(sorted(excluded_hits)),round(ratio,4),reason)
