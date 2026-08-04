from __future__ import annotations
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class MetaTitle:
    text: str
    length: int
    brand_included: bool
    keyword_included: bool
    truncated: bool
    def as_dict(self):return asdict(self)

class MetaTitleBuilder:
    def build(self,title: str,brand: str="") -> str:return self.build_details(title,brand=brand).text
    def build_details(self,title: str,*,brand: str="",keyword: str="",maximum: int=60) -> MetaTitle:
        clean=" ".join(str(title).split());prefix=f"{keyword.strip()} — " if keyword and keyword.casefold() not in clean.casefold() else "";suffix=f" | {brand.strip()}" if brand else "";available=max(1,maximum-len(suffix));base=(prefix+clean);truncated=len(base)>available
        if truncated:base=base[:max(1,available-3)].rsplit(" ",1)[0].rstrip()+"..."
        text=(base+suffix)[:maximum]
        return MetaTitle(text,len(text),bool(brand and brand.casefold() in text.casefold()),bool(keyword and keyword.casefold() in text.casefold()),truncated)
