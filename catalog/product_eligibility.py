from compliance.restricted_product_filter import restricted_reason
def eligibility(product: dict[str,object],minimum_stock: int=10) -> tuple[bool,list[str]]:
    reasons=[]
    reason=restricted_reason(str(product.get("title",""))+" "+str(product.get("description","")))
    if reason: reasons.append(reason)
    if int(product.get("stock",0) or 0)<minimum_stock: reasons.append("Stock fournisseur insuffisant.")
    if float(product.get("price",0) or 0)<=0: reasons.append("Prix fournisseur invalide.")
    return not reasons,reasons
