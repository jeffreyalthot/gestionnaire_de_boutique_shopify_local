from __future__ import annotations
import re
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class CompanyVerification:
    valid: bool
    score: float
    missing: tuple[str,...]
    issues: tuple[str,...]
    normalized: dict[str,object]
    def as_dict(self):return asdict(self)

class CompanyVerifier:
    REQUIRED=("legal_name","registration_id","country_code")
    def verify(self,record: dict[str,object]) -> tuple[bool,tuple[str,...]]:
        result=self.evaluate(record);return result.valid,tuple((*result.missing,*result.issues))
    def evaluate(self,record: dict[str,object]) -> CompanyVerification:
        normalized={**record,"legal_name":" ".join(str(record.get("legal_name","")).split()),"registration_id":re.sub(r"\s+","",str(record.get("registration_id","")).upper()),"country_code":str(record.get("country_code","")).upper()};missing=tuple(x for x in self.REQUIRED if not normalized.get(x));issues=[]
        if normalized.get("country_code") and not re.fullmatch(r"[A-Z]{2}",str(normalized["country_code"])):issues.append("invalid_country_code")
        if normalized.get("website") and not str(normalized["website"]).startswith(("https://","http://")):issues.append("invalid_website")
        if normalized.get("registration_status") in {"inactive","dissolved","suspended"}:issues.append("inactive_company")
        score=max(0,1-len(missing)*.25-len(issues)*.25)
        return CompanyVerification(not missing and not issues,round(score,4),missing,tuple(issues),normalized)
