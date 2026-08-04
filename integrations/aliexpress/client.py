from __future__ import annotations

from typing import Any

from integrations.aliexpress.gateway import AliExpressGateway


class AliExpressClient:
    def __init__(self, gateway: AliExpressGateway) -> None:
        self.gateway = gateway

    async def search_products(self, keyword: str, page: int = 1, page_size: int = 50) -> dict[str, Any]:
        params = {"keyword": keyword, "page": page, "page_size": page_size}
        return await self.gateway.call("/v2/products/search", method="GET", params=params)

    async def get_product(self, product_id: str) -> dict[str, Any]:
        return await self.gateway.call(f"/v2/products/{product_id}", method="GET")

    async def list_orders(self, page: int = 1, page_size: int = 50, status: str | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        if status:
            params["status"] = status
        return await self.gateway.call("/v2/orders", method="GET", params=params)

    async def get_order(self, order_id: str) -> dict[str, Any]:
        return await self.gateway.call(f"/v2/orders/{order_id}", method="GET")

    async def create_order(self, order_payload: dict[str, Any]) -> dict[str, Any]:
        return await self.gateway.call("/v2/orders", method="POST", json_body=order_payload)

    async def cancel_order(self, order_id: str) -> dict[str, Any]:
        return await self.gateway.call("/v2/orders/cancel", method="POST", json_body={"orderId": order_id})

    async def tracking(self, order_id: str) -> dict[str, Any]:
        return await self.gateway.call(f"/v2/logistics/tracking", method="GET", params={"orderId": order_id})

    async def upload_image(self, image_bytes: bytes, filename: str = "image.jpg") -> dict[str, Any]:
        files = {"image": (filename, image_bytes, "image/jpeg")}
        return await self.gateway.call("/v2/images/upload", method="POST", files=files)
