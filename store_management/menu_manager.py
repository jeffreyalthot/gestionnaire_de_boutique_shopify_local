from __future__ import annotations
from dataclasses import asdict,dataclass
from urllib.parse import urlparse

@dataclass(frozen=True,slots=True)
class MenuAudit:
    valid: bool
    issues: tuple[str,...]
    items: int
    maximum_depth: int
    duplicate_urls: tuple[str,...]
    def as_dict(self):return asdict(self)

class MenuManager:
    def validate(self,items: list[dict[str,object]],max_depth: int=3) -> tuple[str,...]:return self.audit(items,max_depth=max_depth).issues
    def audit(self,items: list[dict[str,object]],*,max_depth: int=3,maximum_items: int=200) -> MenuAudit:
        issues=[];urls=[];count=0;deepest=0
        def walk(rows,depth,path):
            nonlocal count,deepest
            deepest=max(deepest,depth)
            if depth>max_depth:issues.append(f"depth_exceeded:{path}");return
            for index,row in enumerate(rows or []):
                count+=1;title=str(row.get("title","")).strip();url=str(row.get("url","")).strip();node=f"{path}/{index}"
                if not title:issues.append(f"missing_title:{node}")
                if not url:issues.append(f"missing_url:{node}")
                elif url.startswith(("javascript:","data:")):issues.append(f"unsafe_url:{node}")
                else:urls.append(url)
                walk(row.get("children",[]) or [],depth+1,node)
        walk(items,1,"root")
        if count>maximum_items:issues.append("too_many_items")
        duplicates=tuple(sorted({url for url in urls if urls.count(url)>1}))
        if duplicates:issues.append("duplicate_urls")
        return MenuAudit(not issues,tuple(issues),count,deepest,duplicates)
