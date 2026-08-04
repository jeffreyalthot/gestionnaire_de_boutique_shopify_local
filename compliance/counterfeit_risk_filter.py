from __future__ import annotations

import re
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class CounterfeitRiskAssessment:
    score: float
    level: str
    indicators: tuple[str,...]
    blocked: bool
    def as_dict(self):return asdict(self)

class CounterfeitRiskFilter:
    PATTERNS={"replica":r"\breplica\b","copy":r"\bcopy\b","one_to_one":r"\b1\s*:\s*1\b","inspired_by":r"\binspired by\b","authentic_like":r"\bauthentic\s*(quality|look)\b","logo_unlicensed":r"\bwith\s+logo\b"}
    def assess(self,text: str,*,authorized: bool=False) -> CounterfeitRiskAssessment:
        hits=tuple(name for name,pattern in self.PATTERNS.items() if re.search(pattern,str(text),re.I)); score=0 if authorized else min(1.0,len(hits)*.28); level="low" if score<.25 else "medium" if score<.5 else "high" if score<.8 else "critical"
        return CounterfeitRiskAssessment(round(score,4),level,hits,score>=.5)

def counterfeit_risk(text: str) -> float:return CounterfeitRiskFilter().assess(text).score
