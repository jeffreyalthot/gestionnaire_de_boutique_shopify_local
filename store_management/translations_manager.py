import re
from store_management.mutation_plan import MutationPlan
class TranslationsManager:
    def mutations(self,resource_id: str,locale: str,translations: dict[str,str]) -> tuple[dict[str,str],...]:
        if not resource_id:raise ValueError("resource_id requis")
        if not re.fullmatch(r"[a-z]{2}(?:-[A-Z]{2})?",locale):raise ValueError("locale invalide")
        rows=[]
        for key,value in sorted(translations.items()):
            value=str(value).strip()
            if value:rows.append({"resourceId":resource_id,"locale":locale,"key":str(key),"value":value})
        return tuple(rows)
    def plan(self,*args,**kwargs) -> tuple[dict[str,object],...]:return tuple(MutationPlan("translation","register",row).to_dict() for row in self.mutations(*args,**kwargs))
