from __future__ import annotations
import hashlib
from dataclasses import asdict,dataclass
from datetime import datetime,timezone
from ai.language.text_sanitizer import sanitize_html

@dataclass(frozen=True,slots=True)
class EmailCampaignDraft:
    name: str
    subject: str
    preview_text: str
    body: str
    segment: str
    status: str
    fingerprint: str
    created_at: str
    warnings: tuple[str,...]
    def as_dict(self):return asdict(self)

class CampaignBuilder:
    def build(self,*,name: str,subject: str,body: str,segment: str) -> dict[str,object]:return self.prepare(name=name,subject=subject,body=body,segment=segment).as_dict()
    def prepare(self,*,name: str,subject: str,body: str,segment: str,preview_text: str="") -> EmailCampaignDraft:
        clean_subject=" ".join(str(subject).split())[:150];clean_body=str(body).strip();clean_name=" ".join(str(name).split())[:120];segment=str(segment).strip() or "all_consented"
        if not clean_subject or not clean_body:raise ValueError("contenu requis")
        warnings=[];plain=sanitize_html(clean_body,50000)
        if len(clean_subject)>60:warnings.append("long_subject")
        if len(plain)<80:warnings.append("short_body")
        preview=(preview_text.strip() or plain[:120])[:150];fingerprint=hashlib.sha256(f"{clean_subject}|{clean_body}|{segment}".encode()).hexdigest()[:20]
        return EmailCampaignDraft(clean_name,clean_subject,preview,clean_body,segment,"draft",fingerprint,datetime.now(timezone.utc).isoformat(),tuple(warnings))
