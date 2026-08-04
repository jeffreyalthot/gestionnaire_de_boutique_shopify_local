from __future__ import annotations
import hashlib,re,unicodedata
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class UrlHandle:
    handle: str
    changed: bool
    collision_suffix: str
    valid: bool
    def as_dict(self):return asdict(self)

class UrlHandleBuilder:
    def build(self,text: str) -> str:return self.build_details(text).handle
    def build_details(self,text: str,*,existing: set[str]|None=None,maximum: int=255) -> UrlHandle:
        ascii_text=unicodedata.normalize("NFKD",str(text)).encode("ascii","ignore").decode().lower();base=re.sub(r"-+","-",re.sub(r"[^a-z0-9]+","-",ascii_text)).strip("-")[:maximum]
        if not base:base="item"
        handle=base;suffix="";existing=existing or set()
        if handle in existing:
            suffix=hashlib.sha256(str(text).encode()).hexdigest()[:6];handle=f"{base[:max(1,maximum-7)]}-{suffix}"
        return UrlHandle(handle,handle!=text,suffix,bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",handle)))
