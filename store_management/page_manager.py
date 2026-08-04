from store_management.mutation_plan import MutationPlan,clean_handle
class PageManager:
    def draft(self,title: str,body: str,handle: str) -> dict[str,object]:
        title=title.strip();body=body.strip();handle=clean_handle(handle or title)
        if not title or not body:raise ValueError("titre et contenu requis")
        return {"title":title,"body":body,"handle":handle,"published":False}
    def plan(self,title: str,body: str,handle: str="") -> MutationPlan:return MutationPlan("page","upsert",self.draft(title,body,handle))
