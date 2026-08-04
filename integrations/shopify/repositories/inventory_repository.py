from __future__ import annotations

from typing import Any

from integrations.shopify.repositories.base_repository import ShopifyRepository


class InventoryRepository(ShopifyRepository):
    resource = "inventory"

    async def set_quantities(self, quantities: list[dict[str, Any]], *, name: str = "available",
                             reason: str = "correction") -> dict[str, Any]:
        if not quantities:
            raise ValueError("at least one inventory quantity is required")
        return await self._call("set_quantities", self.client.inventory_set, name, reason, quantities)
