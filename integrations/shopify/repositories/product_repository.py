from __future__ import annotations

from typing import Any

from integrations.shopify.mappers.product_mapper import map_shopify_product
from integrations.shopify.repositories.base_repository import ShopifyRepository


class ProductRepository(ShopifyRepository):
    resource = "products"

    async def list_page(self, *, first: int = 50, after: str | None = None, query: str = "") -> dict[str, object]:
        page = await self._call("list", self.client.products, first, after, query)
        edges = page.get("edges", []) if isinstance(page, dict) else []
        items = [map_shopify_product(edge.get("node", {})) for edge in edges if isinstance(edge, dict)]
        return {"items": items, "page_info": dict(page.get("pageInfo", {})), "count": len(items)}

    async def get(self, product_id: str) -> dict[str, object] | None:
        node = await self._call("get", self.client.product_by_id, product_id)
        return map_shopify_product(node) if isinstance(node, dict) else None

    async def upsert(self, product_input: dict[str, Any], *, synchronous: bool = True) -> dict[str, Any]:
        return await self._call("upsert", self.client.product_set, product_input, synchronous)

    async def publish(self, product_id: str, publication_id: str) -> dict[str, Any]:
        return await self._call("publish", self.client.publish, product_id, publication_id)
