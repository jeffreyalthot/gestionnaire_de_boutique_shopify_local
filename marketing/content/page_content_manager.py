from __future__ import annotations

import hashlib,re
from dataclasses import asdict,dataclass
from datetime import datetime,timezone
from ai.language.text_sanitizer import sanitize_html

@dataclass(frozen=True,slots=True)
class PageContent:
    title: str
    body: str
    handle: str
    seo_title: str
    meta_description: str
    fingerprint: str
    updated_at: str
    def as_dict(self):return asdict(self)

class PageContentManager:
    def normalize(self,title: str,body: str) -> dict[str,str]:return self.prepare(title,body).as_dict()
    def prepare(self,title: str,body: str,*,handle: str="",seo_title: str="",meta_description: str="") -> PageContent:
        clean_title=" ".join(str(title).split())[:255]; clean_body=str(body).strip()
        if not clean_title:raise ValueError("titre de page requis")
        plain=sanitize_html(clean_body,10000); auto_handle=re.sub(r"[^a-z0-9]+","-",clean_title.lower()).strip("-")[:255]
        resolved_handle=(handle.strip() or auto_handle); resolved_seo=(seo_title.strip() or clean_title)[:70]; resolved_meta=(meta_description.strip() or plain)[:160]
        fingerprint=hashlib.sha256(f"{clean_title}|{clean_body}|{resolved_handle}".encode()).hexdigest()[:20]
        return PageContent(clean_title,clean_body,resolved_handle,resolved_seo,resolved_meta,fingerprint,datetime.now(timezone.utc).isoformat())
    def diff(self,current: dict[str,object],desired: PageContent) -> dict[str,tuple[object,object]]:
        target=desired.as_dict();return {k:(current.get(k),v) for k,v in target.items() if k not in {"updated_at","fingerprint"} and current.get(k)!=v}
