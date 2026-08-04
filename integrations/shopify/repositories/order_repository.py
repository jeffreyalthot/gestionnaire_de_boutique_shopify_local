from __future__ import annotations

from integrations.shopify.mappers.order_mapper import map_shopify_order
from integrations.shopify.repositories.base_repository import ShopifyRepository


class OrderRepository(ShopifyRepository):
    resource = "orders"

    async def list_page(self, *, first: int = 50, after: str | None = None, query: str = "") -> dict[str, object]:
        page = await self._call("list", self.client.orders, first, after, query)
        edges = page.get("edges", []) if isinstance(page, dict) else []
        items = [map_shopify_order(edge.get("node", {})) for edge in edges if isinstance(edge, dict)]
        return {"items": items, "page_info": dict(page.get("pageInfo", {})), "count": len(items)}

    async def get(self, order_id: str) -> dict[str, object] | None:
        node = await self._call("get", self.client.order, order_id)
        return map_shopify_order(node) if isinstance(node, dict) else None
