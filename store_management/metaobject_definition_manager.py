from store_management.mutation_plan import MutationPlan,clean_handle
class MetaobjectDefinitionManager:
    def definition(self,name: str,type_name: str,fields: list[dict[str,str]]) -> dict[str,object]:
        name=name.strip();type_name=clean_handle(type_name)
        if not name or not type_name or not fields:raise ValueError("nom, type et champs requis")
        keys=set();normalized=[]
        for field in fields:
            key=clean_handle(str(field.get("key",field.get("name",""))))
            if not key or key in keys:raise ValueError("champ invalide ou dupliqué")
            keys.add(key);normalized.append({"name":str(field.get("name",key)).strip(),"key":key,"type":str(field.get("type","single_line_text_field"))})
        return {"name":name,"type":type_name,"fieldDefinitions":normalized}
    def plan(self,*args,**kwargs) -> MutationPlan:return MutationPlan("metaobject_definition","create",self.definition(*args,**kwargs),approval_required=True)
