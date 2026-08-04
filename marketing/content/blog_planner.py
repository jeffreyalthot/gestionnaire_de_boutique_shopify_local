from __future__ import annotations

from dataclasses import asdict,dataclass
from datetime import date,timedelta

@dataclass(frozen=True,slots=True)
class BlogPlanItem:
    keyword: str
    linked_products: tuple[str,...]
    working_title: str
    publish_date: str
    intent: str
    priority: float
    outline: tuple[str,...]
    def as_dict(self):return asdict(self)

class BlogPlanner:
    def plan(self,keywords: list[str],products: list[str],limit: int=10) -> tuple[dict[str,object],...]:
        return tuple(item.as_dict() for item in self.detailed_plan(keywords,products,limit=limit))
    def detailed_plan(self,keywords: list[str],products: list[str],*,limit: int=10,start: date|None=None,cadence_days: int=7) -> tuple[BlogPlanItem,...]:
        start=start or date.today();seen=set();result=[]
        for index,raw in enumerate(keywords):
            keyword=" ".join(str(raw).split()).lower()
            if not keyword or keyword in seen:continue
            seen.add(keyword); intent="commercial" if any(word in keyword for word in ("best","buy","price","meilleur")) else "informational"
            priority=max(.1,1-index/max(1,len(keywords)));linked=tuple(dict.fromkeys(map(str,products)))[:3]
            result.append(BlogPlanItem(keyword,linked,f"Guide: {keyword.title()}",(start+timedelta(days=len(result)*max(1,cadence_days))).isoformat(),intent,round(priority,4),("Introduction",f"Comment choisir {keyword}","Comparaison","FAQ")))
            if len(result)>=limit:break
        return tuple(result)
