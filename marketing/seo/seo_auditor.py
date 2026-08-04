from __future__ import annotations
import re
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class SEOAuditResult:
    valid: bool
    score: float
    issues: tuple[str,...]
    warnings: tuple[str,...]
    recommendations: tuple[str,...]
    metrics: dict[str,object]
    def as_dict(self):return asdict(self)

class SEOAuditor:
    def audit(self,*,title: str,description: str,handle: str,keyword: str="",image_alt_texts: tuple[str,...]=(),canonical_url: str="") -> dict[str,object]:return self.evaluate(title=title,description=description,handle=handle,keyword=keyword,image_alt_texts=image_alt_texts,canonical_url=canonical_url).as_dict()
    def evaluate(self,**data: object) -> SEOAuditResult:
        title=" ".join(str(data.get("title","")).split());description=" ".join(str(data.get("description","")).split());handle=str(data.get("handle","")).strip();keyword=str(data.get("keyword","")).strip().casefold();issues=[];warnings=[];recommendations=[]
        if not 30<=len(title)<=60:issues.append("title_length")
        if not 80<=len(description)<=160:issues.append("description_length")
        if not handle or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",handle):issues.append("invalid_handle")
        if keyword and keyword not in title.casefold():warnings.append("keyword_missing_title")
        if keyword and keyword not in description.casefold():warnings.append("keyword_missing_description")
        alt=tuple(str(x).strip() for x in data.get("image_alt_texts",()) if str(x).strip())
        if not alt:warnings.append("missing_image_alt")
        if data.get("canonical_url") and not str(data["canonical_url"]).startswith(("https://","http://")):issues.append("invalid_canonical")
        recommendations.extend(issue.replace("invalid_","fix_").replace("_length","_length_optimize") for issue in (*issues,*warnings));score=max(0,1-len(issues)*.25-len(warnings)*.08)
        return SEOAuditResult(not issues,round(score,4),tuple(issues),tuple(warnings),tuple(recommendations),{"title_length":len(title),"description_length":len(description),"alt_count":len(alt)})
