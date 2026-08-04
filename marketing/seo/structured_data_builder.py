from __future__ import annotations
from decimal import Decimal, InvalidOperation
class StructuredDataBuilder:
    def product(self, product: dict[str, object]) -> dict[str, object]:
        title = str(product.get("title", "")).strip()
        if not title:
            raise ValueError("Le titre produit est requis pour les données structurées.")
        try:
            price = Decimal(str(product.get("price_cad", product.get("price", 0)))).quantize(Decimal("0.01"))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("Prix produit invalide.") from exc
        stock = int(product.get("stock", 0) or 0)
        offer: dict[str, object] = {
            "@type": "Offer", "price": str(price), "priceCurrency": str(product.get("currency", "CAD")).upper(),
            "availability": "https://schema.org/InStock" if stock > 0 else "https://schema.org/OutOfStock",
            "itemCondition": "https://schema.org/NewCondition",
        }
        if product.get("url"): offer["url"] = str(product["url"])
        result: dict[str, object] = {"@context": "https://schema.org", "@type": "Product", "name": title, "offers": offer}
        for source, target in (("sku", "sku"), ("description", "description"), ("image", "image"), ("gtin", "gtin")):
            if product.get(source): result[target] = product[source]
        if product.get("brand"): result["brand"] = {"@type": "Brand", "name": str(product["brand"])}
        return result
