from __future__ import annotations
import re
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class BrandVoiceAssessment:
    valid: bool
    issues: tuple[str,...]
    tone_score: float
    readability_score: float
    suggestions: tuple[str,...]
    def as_dict(self):return asdict(self)

class BrandVoicePolicy:
    BANNED=("guaranteed cure","risk free","best in the world")
    def validate(self,text: str) -> tuple[bool,tuple[str,...]]:
        result=self.assess(text);return result.valid,result.issues
    def assess(self,text: str,*,preferred_terms: tuple[str,...]=(),maximum_sentence_words: int=30) -> BrandVoiceAssessment:
        value=" ".join(str(text).split());lower=value.casefold();issues=[x for x in self.BANNED if x in lower];sentences=[s.strip() for s in re.split(r"[.!?]+",value) if s.strip()];long=sum(len(s.split())>maximum_sentence_words for s in sentences);readability=max(0,1-long/max(1,len(sentences)));preferred_hits=sum(term.casefold() in lower for term in preferred_terms);tone=min(1,.5+preferred_hits*.1-len(issues)*.25);suggestions=[]
        if long:suggestions.append("shorten_sentences")
        if issues:suggestions.append("remove_unsubstantiated_claims")
        return BrandVoiceAssessment(not issues,tuple(issues),round(tone,4),round(readability,4),tuple(suggestions))
