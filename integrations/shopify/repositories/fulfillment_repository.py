from __future__ import annotations

from typing import Any

from integrations.shopify.repositories.base_repository import ShopifyRepository


class FulfillmentRepository(ShopifyRepository):
    resource = "fulfillments"

    async def for_order(self, order_id: str) -> list[dict[str, Any]]:
        return list(await self._call("for_order", self.client.fulfillment_orders, order_id))

    async def create(self, fulfillment_order_id: str, tracking: dict[str, Any], *,
                     notify_customer: bool = True) -> dict[str, Any]:
        return await self._call("create", self.client.create_fulfillment,
                                fulfillment_order_id, tracking, notify_customer)

    async def update_tracking(self, fulfillment_id: str, tracking: dict[str, Any], *,
                              notify_customer: bool = True) -> dict[str, Any]:
        return await self._call("update_tracking", self.client.update_tracking,
                                fulfillment_id, tracking, notify_customer)
