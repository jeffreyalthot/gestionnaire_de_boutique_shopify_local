from __future__ import annotations

from integrations.shopify.mappers.base import gid, mapping, timestamp


def map_inventory_level(node: dict[str, object]) -> dict[str, object]:
    quantities: dict[str, int] = {}
    for item in node.get("quantities", []) or []:
        source = mapping(item)
        name = str(source.get("name", "") or "").strip().lower()
        if name:
            quantities[name] = int(source.get("quantity", 0) or 0)
    location = mapping(node.get("location"))
    item = mapping(node.get("item", node.get("inventoryItem")))
    available = int(quantities.get("available", 0))
    committed = int(quantities.get("committed", 0))
    reserved = int(quantities.get("reserved", 0))
    on_hand = int(quantities.get("on_hand", quantities.get("onhand", available + committed + reserved)))
    return {
        "id": gid(node.get("id"), "InventoryLevel"),
        "gid": str(node.get("id", "") or ""),
        "quantities": dict(sorted(quantities.items())),
        "available": available,
        "committed": committed,
        "reserved": reserved,
        "incoming": int(quantities.get("incoming", 0)),
        "on_hand": on_hand,
        "sellable": max(0, available - reserved),
        "location": location,
        "location_id": gid(location.get("id"), "Location"),
        "item": item,
        "inventory_item_id": gid(item.get("id"), "InventoryItem"),
        "updated_at": timestamp(node.get("updatedAt")),
    }
