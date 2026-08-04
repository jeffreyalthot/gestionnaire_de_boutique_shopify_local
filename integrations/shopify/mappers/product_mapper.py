from __future__ import annotations

from typing import Any

from integrations.shopify.mappers.base import gid, mapping, nodes, pagination, string_tuple, timestamp
from integrations.shopify.mappers.variant_mapper import map_variant


def map_shopify_product(node: dict[str, object]) -> dict[str, object]:
    variants_container = mapping(node.get("variants"))
    media_container = mapping(node.get("media"))
    collections_container = mapping(node.get("collections"))
    options = []
    for option in nodes(node.get("options", ())):
        options.append({
            "id": gid(option.get("id"), "ProductOption"),
            "name": str(option.get("name", "") or ""),
            "position": int(option.get("position", 0) or 0),
            "values": string_tuple(option.get("values", ())),
        })
    return {
        "id": gid(node.get("id"), "Product"),
        "gid": str(node.get("id", "") or ""),
        "title": str(node.get("title", "") or "").strip(),
        "description_html": str(node.get("descriptionHtml", node.get("description", "")) or ""),
        "status": str(node.get("status", "") or "").lower(),
        "handle": str(node.get("handle", "") or ""),
        "vendor": str(node.get("vendor", "") or ""),
        "product_type": str(node.get("productType", "") or ""),
        "tags": string_tuple(node.get("tags", ())),
        "created_at": timestamp(node.get("createdAt")),
        "updated_at": timestamp(node.get("updatedAt")),
        "published_at": timestamp(node.get("publishedAt")),
        "online_store_url": str(node.get("onlineStoreUrl", "") or ""),
        "total_inventory": int(node.get("totalInventory", 0) or 0),
        "tracks_inventory": bool(node.get("tracksInventory", True)),
        "options": tuple(options),
        "variants": tuple(map_variant(item) for item in nodes(variants_container)),
        "variant_pagination": pagination(variants_container),
        "media": tuple(nodes(media_container)),
        "media_pagination": pagination(media_container),
        "collections": tuple({"id": gid(item.get("id"), "Collection"), "title": str(item.get("title", ""))} for item in nodes(collections_container)),
        "raw": dict(node),
    }
