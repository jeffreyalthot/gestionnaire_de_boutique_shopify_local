from __future__ import annotations

from app.version import VERSION


def render_orders(state: dict[str, object], width: int = 94) -> list[str]:
    counts=state["counts"]; queue=state["queue"]; control=state.get("commerce_control", {})
    return [
        f"SHOPIFY - ALIBABA AUTOMATION MANAGER {VERSION} | PAGE 3/8 ORDERS",
        "="*width,
        f"Orders={counts.get('orders',0)} Paid={counts.get('paid_orders',0)} Pending procurement={counts.get('pending_procurement',0)}",
        f"Queue pending={queue.get('pending',0)} leased={queue.get('leased',0)} dead={queue.get('dead',0)}",
        f"Purchase intents={control.get('purchase_intents_pending',0)} Reserved units={control.get('reserved_units',0)} Risk holds={control.get('risk_holds',0)}",
        "-"*width,
        "INTAKE: webhook HMAC -> replay guard -> normalization -> PII vault -> accounting event",
        "RISK: amount, address mismatch, velocity, proxy, country, payment history, customer history",
        "ROUTING: await_payment | risk_review | mapping_exception | procurement | cancelled",
        "SUPPLIER SPLIT: one group per supplier with product/SKU/quantity validation.",
        "PURCHASE: stock/price/freight recheck -> approval -> create order -> payment -> confirmation.",
        "IDEMPOTENCY: webhook external ID, task key, supplier-order key, payment reference.",
        "-"*width,
        "EXCEPTIONS: missing mapping | out of stock | changed price | freight drift | supplier failure",
        "COMPENSATION: hold order, alternate supplier, customer contact, partial refund, full cancellation",
    ]
