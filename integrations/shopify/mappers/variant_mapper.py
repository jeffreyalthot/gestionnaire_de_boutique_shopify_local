from __future__ import annotations

from integrations.shopify.mappers.base import decimal_value, gid, mapping, money, string_tuple


def map_variant(node: dict[str, object]) -> dict[str, object]:
    price, currency = money(node.get("price", 0))
    compare_at, _ = money(node.get("compareAtPrice", 0), default_currency=currency)
    inventory_item = mapping(node.get("inventoryItem"))
    product = mapping(node.get("product"))
    options = []
    for item in node.get("selectedOptions", []) or []:
        option = mapping(item)
        options.append({"name": str(option.get("name", "") or ""), "value": str(option.get("value", "") or "")})
    return {
        "id": gid(node.get("id"), "ProductVariant"),
        "gid": str(node.get("id", "") or ""),
        "product_id": gid(product.get("id"), "Product"),
        "title": str(node.get("title", "") or ""),
        "sku": str(node.get("sku", "") or "").strip(),
        "barcode": str(node.get("barcode", "") or "").strip(),
        "price": price,
        "currency": currency,
        "compare_at_price": compare_at,
        "stock": int(node.get("inventoryQuantity", 0) or 0),
        "available_for_sale": bool(node.get("availableForSale", False)),
        "inventory_policy": str(node.get("inventoryPolicy", "") or "").lower(),
        "inventory_item_id": gid(inventory_item.get("id"), "InventoryItem"),
        "requires_shipping": bool(node.get("requiresShipping", True)),
        "taxable": bool(node.get("taxable", True)),
        "weight": float(node.get("weight", 0) or 0),
        "weight_unit": str(node.get("weightUnit", "") or "").lower(),
        "options": tuple(options),
        "option_values": string_tuple(option["value"] for option in options),
    }
