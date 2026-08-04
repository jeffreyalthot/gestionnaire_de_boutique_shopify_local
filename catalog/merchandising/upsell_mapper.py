from __future__ import annotations


class UpsellMapper:
    def map(self, products: list[dict[str, object]], *, maximum: int = 3) -> dict[str, tuple[str, ...]]:
        by_category: dict[str, list[dict[str, object]]] = {}
        for product in products:
            by_category.setdefault(str(product.get("category", "")), []).append(product)
        result: dict[str, tuple[str, ...]] = {}
        for product in products:
            identifier = str(product.get("id", "")); price = float(product.get("sale_price_cad", 0.0) or 0.0)
            candidates = sorted((item for item in by_category.get(str(product.get("category", "")), [])
                                 if str(item.get("id", "")) != identifier
                                 and price < float(item.get("sale_price_cad", 0.0) or 0.0) <= price * 1.6),
                                key=lambda item: (-float(item.get("score", 0.0) or 0.0), float(item.get("sale_price_cad", 0.0) or 0.0)))
            result[identifier] = tuple(str(item.get("id", "")) for item in candidates[:maximum])
        return result
