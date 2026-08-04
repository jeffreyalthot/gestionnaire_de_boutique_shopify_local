from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from hashlib import sha256
from typing import Any

@dataclass(frozen=True, slots=True)
class ChannelValidation:
    valid: bool
    issues: tuple[str,...]

class ProductFeedAdapter:
    channel="generic"
    max_title=150
    required=("id","title","description","url","image_url","price_cad")
    def _money(self,value: object) -> str:
        amount=Decimal(str(value or 0)).quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)
        return f"{amount:.2f} CAD"
    def validate(self,p: dict[str,object]) -> ChannelValidation:
        issues=[f"missing:{k}" for k in self.required if p.get(k) in (None,"")]
        if int(p.get("stock",0) or 0)<0:issues.append("negative_stock")
        if float(p.get("price_cad",0) or 0)<=0:issues.append("invalid_price")
        return ChannelValidation(not issues,tuple(issues))
    def map_product(self,p: dict[str,object]) -> dict[str,object]:
        validation=self.validate(p)
        title=str(p.get("title","")).strip()[:self.max_title]
        payload={"id":str(p.get("id","")),"title":title,"description":str(p.get("description","")).strip(),"link":str(p.get("url","")),"image_link":str(p.get("image_url","")),"availability":"in_stock" if int(p.get("stock",0) or 0)>0 else "out_of_stock","price":self._money(p.get("price_cad",0)),"brand":str(p.get("brand") or p.get("vendor") or "Generic"),"condition":str(p.get("condition") or "new"),"channel":self.channel,"validation_issues":validation.issues}
        payload["content_hash"]=sha256(repr(sorted(payload.items())).encode()).hexdigest()
        return payload
