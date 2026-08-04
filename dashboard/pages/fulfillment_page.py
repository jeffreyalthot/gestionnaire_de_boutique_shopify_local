from __future__ import annotations

from app.version import VERSION


def render_fulfillment(state: dict[str, object], width: int = 94) -> list[str]:
    counts=state["counts"]
    return [
        f"SHOPIFY - ALIBABA AUTOMATION MANAGER {VERSION} | PAGE 4/8 FULFILLMENT",
        "="*width,
        f"Pending procurement={counts.get('pending_procurement',0)} Failed tasks={counts.get('failed_tasks',0)}",
        "-"*width,
        "FLOW: supplier order -> tracking poll/event -> carrier mapping -> Shopify fulfillment -> notify",
        "Tracking events are normalized and deduplicated before updating Shopify.",
        "Delivery promise monitor detects late dispatch, stalled transit, failed delivery and loss.",
        "Customer notifications are planned from event type, locale and SLA without duplicate sends.",
        "Customs payload preserves HS code, origin, value, weight and product description when available.",
        "-"*width,
        "EXCEPTIONS: damaged | lost | undeliverable | address correction | customs delay | partial shipment",
        "RECOVERY: supplier inquiry -> carrier inquiry -> replacement/refund policy -> Shopify reconciliation",
    ]
