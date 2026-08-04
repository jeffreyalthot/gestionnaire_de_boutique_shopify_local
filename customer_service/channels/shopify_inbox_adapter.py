from __future__ import annotations

from typing import Any


class ShopifyInboxAdapter:
    def __init__(self, shopify: Any) -> None:
        self.shopify = shopify

    async def send_order_note(self, order_id: str, note: str) -> dict[str, object]:
        # Les capacités Shopify varient selon l'application; le client central reste l'unique transport.
        method = getattr(self.shopify, "update_order_note", None)
        if method is None:
            return {"status": "unsupported", "order_id": order_id}
        result = method(order_id, note[:5000])
        if hasattr(result, "__await__"):
            result = await result
        return {"status": "sent", "result": result}
