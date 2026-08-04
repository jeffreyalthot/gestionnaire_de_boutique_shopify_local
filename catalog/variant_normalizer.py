from decimal import Decimal
def normalize_variants(skus: list[dict[str,object]],product_id: str) -> list[dict[str,object]]:
    result=[]
    for index,sku in enumerate(skus):
        supplier_sku=str(sku.get("skuId") or sku.get("sku_id") or sku.get("id") or index)
        attrs=sku.get("attributes") or sku.get("options") or {}
        result.append({"supplier_sku_id":supplier_sku,"sku":f"ALI-{product_id}-{supplier_sku}",
                       "options":attrs,"cost":Decimal(str(sku.get("price") or sku.get("unitPrice") or 0)),
                       "stock":int(sku.get("stock") or sku.get("inventory") or 0)})
    return result
