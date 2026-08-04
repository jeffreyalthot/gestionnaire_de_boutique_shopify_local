from __future__ import annotations

from integrations.shopify.mappers.base import gid, mapping, nodes, timestamp


def map_fulfillment(node: dict[str, object]) -> dict[str, object]:
    tracking_entries = []
    seen: set[tuple[str, str]] = set()
    for raw in node.get("trackingInfo", []) or []:
        item = mapping(raw)
        number = str(item.get("number", "") or "").strip()
        company = str(item.get("company", "") or "").strip()
        key = (company.lower(), number.lower())
        if key in seen:
            continue
        seen.add(key)
        tracking_entries.append({
            "company": company,
            "number": number,
            "url": str(item.get("url", "") or ""),
        })
    order = mapping(node.get("order"))
    fulfillment_order = mapping(node.get("fulfillmentOrder"))
    return {
        "id": gid(node.get("id"), "Fulfillment"),
        "gid": str(node.get("id", "") or ""),
        "status": str(node.get("status", "") or "").lower(),
        "display_status": str(node.get("displayStatus", "") or "").lower(),
        "tracking": tuple(tracking_entries),
        "created_at": timestamp(node.get("createdAt")),
        "updated_at": timestamp(node.get("updatedAt")),
        "delivered_at": timestamp(node.get("deliveredAt")),
        "in_transit_at": timestamp(node.get("inTransitAt")),
        "estimated_delivery_at": timestamp(node.get("estimatedDeliveryAt")),
        "order_id": gid(order.get("id"), "Order"),
        "fulfillment_order_id": gid(fulfillment_order.get("id"), "FulfillmentOrder"),
        "line_items": tuple(nodes(node.get("fulfillmentLineItems", ()))),
        "requires_shipping": bool(node.get("requiresShipping", True)),
    }
