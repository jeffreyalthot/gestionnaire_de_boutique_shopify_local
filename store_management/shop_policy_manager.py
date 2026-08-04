class ShopPolicyManager:
    REQUIRED=("refund","privacy","terms","shipping")
    def completeness(self,policies: dict[str,str]) -> dict[str,object]:
        missing=tuple(x for x in self.REQUIRED if not policies.get(x,"").strip()); return {"complete":not missing,"missing":missing}
