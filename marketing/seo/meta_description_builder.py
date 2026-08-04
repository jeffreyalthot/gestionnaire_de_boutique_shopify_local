from __future__ import annotations
import re
from dataclasses import asdict,dataclass
from ai.language.text_sanitizer import sanitize_html

@dataclass(frozen=True,slots=True)
class MetaDescription:
    text: str
    length: int
    truncated: bool
    keyword_included: bool
    def as_dict(self):return asdict(self)

class MetaDescriptionBuilder:
    def build(self,text: str) -> str:return self.build_details(text).text
    def build_details(self,text: str,*,keyword: str="",minimum: int=80,maximum: int=160,call_to_action: str="") -> MetaDescription:
        cleaned=" ".join(sanitize_html(text,1000).split());candidate=cleaned
        if keyword and keyword.casefold() not in candidate.casefold():candidate=f"{keyword.strip()}. {candidate}".strip()
        if call_to_action and len(candidate)+len(call_to_action)+1<=maximum:candidate=f"{candidate} {call_to_action.strip()}".strip()
        truncated=len(candidate)>maximum
        if truncated:candidate=candidate[:max(0,maximum-3)].rsplit(" ",1)[0].rstrip(" ,.;")+"..."
        return MetaDescription(candidate,len(candidate),truncated,bool(keyword and keyword.casefold() in candidate.casefold()))
