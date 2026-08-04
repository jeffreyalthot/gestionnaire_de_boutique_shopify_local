from __future__ import annotations
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class InternalLinkSuggestion:
    url: str
    score: float
    matched_tags: tuple[str,...]
    anchor_text: str
    def as_dict(self):return asdict(self)

class InternalLinkBuilder:
    def suggest(self,source_tags: set[str],targets: list[dict[str,object]],limit: int=5) -> tuple[str,...]:return tuple(item.url for item in self.rank(source_tags,targets,limit=limit))
    def rank(self,source_tags: set[str],targets: list[dict[str,object]],*,limit: int=5,current_url: str="") -> tuple[InternalLinkSuggestion,...]:
        source={str(tag).strip().lower() for tag in source_tags};result=[]
        for target in targets:
            url=str(target.get("url","")).strip();tags={str(tag).strip().lower() for tag in target.get("tags",())};matches=source&tags
            if not url or url==current_url or not matches:continue
            authority=max(0,min(1,float(target.get("authority",.5) or .5)));score=len(matches)*.7+authority*.3;anchor=str(target.get("title") or next(iter(sorted(matches))))[:120]
            result.append(InternalLinkSuggestion(url,round(score,4),tuple(sorted(matches)),anchor))
        return tuple(sorted(result,key=lambda x:(-x.score,x.url))[:max(0,limit)])
