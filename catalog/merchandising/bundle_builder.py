from __future__ import annotations


def build_bundles(products: list[dict[str, object]], *, maximum: int = 3) -> list[dict[str, object]]:
    by_category: dict[str, list[dict[str, object]]] = {}
    for product in products:
        by_category.setdefault(str(product.get("category", "other")), []).append(product)
    bundles = []
    for category, items in by_category.items():
        eligible = [item for item in items if float(item.get("margin_percent", 0) or 0) >= 40 and int(item.get("stock", 0) or 0) > 0]
        if len(eligible) >= 2:
            selected = eligible[:maximum]
            bundles.append({"category": category, "product_ids": [str(item.get("id")) for item in selected], "discount_percent": 5 if len(selected) == 2 else 8})
    return bundles
