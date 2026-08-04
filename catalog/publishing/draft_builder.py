from __future__ import annotations

from catalog.publishing.product_change_set import ProductChangeSet


class DraftBuilder:
    def build(self, product: dict[str, object]) -> ProductChangeSet:
        return ProductChangeSet(
            product_id=str(product.get("id", "")),
            create=not bool(product.get("shopify_product_id")),
            fields={
                "title": str(product.get("title", ""))[:255],
                "descriptionHtml": str(product.get("descriptionHtml", product.get("description", ""))),
                "productType": str(product.get("product_type", product.get("category", "")))[:100],
                "vendor": str(product.get("vendor", "ELIT21"))[:100],
                "tags": list(product.get("tags", ())),
                "status": "DRAFT",
            },
            variants=tuple(product.get("variants", ())),
            media=tuple(product.get("media", product.get("files", ()))),
        )
