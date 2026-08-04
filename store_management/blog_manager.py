from store_management.mutation_plan import MutationPlan,clean_handle
class BlogManager:
    def article(self,title: str,body: str,tags=(),handle: str="") -> dict[str,object]:
        title=title.strip();body=body.strip()
        if not title or not body:raise ValueError("titre et contenu requis")
        normalized=tuple(sorted({str(x).strip().lower() for x in tags if str(x).strip()}))
        return {"title":title,"body":body,"handle":clean_handle(handle or title),"tags":normalized,"published":False}
    def plan(self,*args,**kwargs) -> MutationPlan:return MutationPlan("article","upsert",self.article(*args,**kwargs))
