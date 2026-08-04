from __future__ import annotations


class VariantDisplayPolicy:
    def order(self, variants: list[dict[str, object]]) -> tuple[dict[str, object], ...]:
        return tuple(sorted(variants, key=lambda item: (
            int(item.get("stock", 0) or 0) <= 0,
            -int(item.get("stock", 0) or 0),
            float(item.get("sale_price_cad", 0.0) or 0.0),
            str(item.get("sku", "")),
        )))
