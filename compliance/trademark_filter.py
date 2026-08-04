from __future__ import annotations

import re
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class TrademarkAssessment:
    matched_brand: str
    risk: str
    authorized: bool
    blocked: bool
    evidence: tuple[str,...]
    def as_dict(self):return asdict(self)

class TrademarkFilter:
    def assess(self,text: str,brands: set[str],*,authorized_brands: set[str]|None=None) -> TrademarkAssessment:
        authorized={brand.casefold() for brand in (authorized_brands or set())}; value=str(text); matches=[]
        for brand in sorted(brands,key=len,reverse=True):
            if re.search(rf"(?<!\w){re.escape(brand)}(?!\w)",value,re.I):matches.append(brand)
        matched=matches[0] if matches else ""; is_authorized=bool(matched and matched.casefold() in authorized)
        return TrademarkAssessment(matched,"high" if matched and not is_authorized else "none",is_authorized,bool(matched and not is_authorized),tuple(matches))

def contains_protected_brand(title: str,brands: set[str]) -> str:return TrademarkFilter().assess(title,brands).matched_brand
