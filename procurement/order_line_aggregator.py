from collections import defaultdict
def aggregate(lines: list[dict[str,object]]) -> list[dict[str,object]]:
    grouped: dict[tuple[str,str],dict[str,object]]={}
    for line in lines:
        key=(str(line.get("supplier_product_id","")),str(line.get("supplier_sku_id","")))
        if key not in grouped:
            grouped[key]={"product_id":key[0],"sku_id":key[1],"quantity":0,"order_line_ids":[]}
        grouped[key]["quantity"]=int(grouped[key]["quantity"])+int(line.get("quantity",0))
        grouped[key]["order_line_ids"].append(str(line.get("id","")))
    return list(grouped.values())
