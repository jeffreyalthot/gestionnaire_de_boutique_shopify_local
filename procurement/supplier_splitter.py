from collections import defaultdict
def split_by_supplier(items: list[dict[str,object]]) -> dict[str,list[dict[str,object]]]:
    result=defaultdict(list)
    for item in items: result[str(item.get("supplier_id","unknown"))].append(item)
    return dict(result)
