from __future__ import annotations


class CrossSellMapper:
    def map(self, products: list[dict[str, object]], *, maximum: int = 4) -> dict[str, tuple[str, ...]]:
        result: dict[str, tuple[str, ...]] = {}
        for product in products:
            identifier = str(product.get("id", ""))
            category = str(product.get("category", ""))
            candidates = [str(item.get("id", "")) for item in products
                          if str(item.get("id", "")) != identifier
                          and str(item.get("category", "")) != category
                          and float(item.get("score", 0.0) or 0.0) >= 0.70]
            result[identifier] = tuple(candidates[:maximum])
        return result
