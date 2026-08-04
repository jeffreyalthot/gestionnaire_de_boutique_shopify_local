from __future__ import annotations
from dataclasses import asdict,dataclass
from marketing.content.brand_voice_policy import BrandVoicePolicy
from marketing.seo.seo_auditor import SEOAuditor

@dataclass(frozen=True,slots=True)
class ProductContentAudit:
    valid: bool
    score: float
    issues: tuple[str,...]
    warnings: tuple[str,...]
    sections: dict[str,object]
    def as_dict(self):return asdict(self)

class ProductContentAuditor:
    def audit(self,product: dict[str,object]) -> dict[str,object]:return self.evaluate(product).as_dict()
    def evaluate(self,product: dict[str,object]) -> ProductContentAudit:
        title=str(product.get("title",""));description=str(product.get("description",product.get("description_html","")));issues=[];warnings=[]
        if not 10<=len(title)<=70:issues.append("title_length")
        if len(description)<80:issues.append("description_too_short")
        voice=BrandVoicePolicy().assess(title+" "+description);issues.extend(f"banned:{x}" for x in voice.issues)
        seo=SEOAuditor().evaluate(title=str(product.get("seo_title",title)),description=str(product.get("meta_description",description)),handle=str(product.get("handle","")),keyword=str(product.get("keyword","")),image_alt_texts=tuple(product.get("image_alt_texts",())))
        issues.extend(f"seo:{x}" for x in seo.issues);warnings.extend(f"seo:{x}" for x in seo.warnings)
        if not product.get("images"):warnings.append("missing_images")
        if not product.get("vendor"):warnings.append("missing_vendor")
        score=max(0,1-len(issues)*.15-len(warnings)*.04)
        return ProductContentAudit(not issues,round(score,4),tuple(dict.fromkeys(issues)),tuple(dict.fromkeys(warnings)),{"voice":voice.as_dict(),"seo":seo.as_dict()})
