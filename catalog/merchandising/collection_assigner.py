from __future__ import annotations


def assign_collections(product: dict[str, object]) -> list[str]:
    collections = []
    category = str(product.get("category", "")).strip()
    if category: collections.append(category)
    if bool(product.get("new")): collections.append("New arrivals")
    if float(product.get("score", 0) or 0) >= .85: collections.append("Best picks")
    if float(product.get("sale_price_cad", 0) or 0) < 25: collections.append("Under 25 CAD")
    return list(dict.fromkeys(collections))
