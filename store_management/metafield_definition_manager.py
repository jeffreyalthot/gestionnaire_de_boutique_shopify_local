import re
from store_management.mutation_plan import MutationPlan
class MetafieldDefinitionManager:
    VALID_TYPES={"single_line_text_field","multi_line_text_field","number_integer","number_decimal","boolean","date","date_time","json","url","product_reference","list.single_line_text_field"}
    def definition(self,namespace: str,key: str,type_name: str,owner_type: str="PRODUCT") -> dict[str,str]:
        namespace=namespace.strip();key=key.strip();type_name=type_name.strip();owner_type=owner_type.strip().upper()
        if not re.fullmatch(r"[a-zA-Z0-9_-]{3,255}",namespace):raise ValueError("namespace invalide")
        if not re.fullmatch(r"[a-zA-Z0-9_-]{2,64}",key):raise ValueError("clé invalide")
        if type_name not in self.VALID_TYPES:raise ValueError("type de métachamp non autorisé")
        return {"namespace":namespace,"key":key,"type":type_name,"ownerType":owner_type}
    def plan(self,*args,**kwargs) -> MutationPlan:return MutationPlan("metafield_definition","create",self.definition(*args,**kwargs),approval_required=True)
