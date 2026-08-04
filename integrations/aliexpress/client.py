"""High-level AliExpress client used for delegation from AlibabaClient.

Implements a minimal set of methods that AlibabaClient expects when it
creates an AliExpress delegate. Each method calls the AliExpressGateway which
wraps the REST v2 Open Platform endpoints.
"""

from __future__ import annotations

from typing import Any

from integrations.aliexpress.gateway import AliExpressGateway


class AliExpressClient:
    def __init__(self, gateway: AliExpressGateway) -> None:
        self.gateway = gateway

    async def search_products(self, keyword: str, page: int = 1, page_size: int = 50) -> dict[str, Any]:
        params = {"keyword": keyword, "page": page, "pageSize": page_size}
        return await self.gateway.request("/v2/products/search", method="GET", params=params)

    async def get_product(self, product_id: str) -> dict[str, Any]:
        return await self.gateway.request(f"/v2/products/{product_id}", method="GET")

    async def get_product_inventory(self, product_id: str) -> dict[str, Any]:
        # AliExpress exposes inventory endpoints; try the product-specific path
        return await self.gateway.request(f"/v2/inventory/{product_id}", method="GET")

    async def create_order(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self.gateway.request("/v2/orders", method="POST", json=payload)

    async def list_orders(self, page: int = 1, page_size: int = 50, status: str | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"page": page, "pageSize": page_size}
        if status:
            params["status"] = status
        return await self.gateway.request("/v2/orders", method="GET", params=params)

    async def get_order(self, order_id: str) -> dict[str, Any]:
        return await self.gateway.request(f"/v2/orders/{order_id}", method="GET")

    async def tracking(self, order_id: str) -> dict[str, Any]:
        # Use the tracking endpoint; the API supports a dedicated tracking path
        params = {"orderId": order_id}
        return await self.gateway.request("/v2/orders/tracking", method="GET", params=params)

