"""AliExpress integration - client implementation.

This client provides a simple, stable surface compatible with the existing
AlibabaClient delegation. It implements only the methods used by the rest of
the application (search_products, get_product, get_product_inventory,
create_order, list_orders, get_order, tracking, upload_image).

The implementation intentionally keeps behavior simple and defensive so it
is ready-to-use and easy to extend.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from config.settings import get_settings
from integrations.aliexpress.gateway import AliExpressGateway


class AliExpressClient:
    def __init__(self, gateway: Optional[AliExpressGateway] = None) -> None:
        self.settings = get_settings()
        self.gateway = gateway or AliExpressGateway(self.settings)

    async def search_products(self, keyword: str, page: int = 1, page_size: int = 50) -> Dict[str, Any]:
        params = {"keyword": keyword, "page": page, "page_size": page_size}
        return await self.gateway.call("/v2/products/search", params)

    async def get_product(self, product_id: str) -> Dict[str, Any]:
        path = f"/v2/products/{product_id}"
        return await self.gateway.call(path, method="GET")

    async def get_product_inventory(self, product_id: str) -> Dict[str, Any]:
        params = {"productId": product_id}
        return await self.gateway.call("/v2/products/inventory", params)

    async def create_order(self, order_payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self.gateway.call("/v2/orders", body=order_payload, method="POST")

    async def list_orders(self, page: int = 1, page_size: int = 50, status: Optional[str] = None) -> Dict[str, Any]:
        params = {"page": page, "page_size": page_size}
        if status:
            params["status"] = status
        return await self.gateway.call("/v2/orders", params)

    async def get_order(self, order_id: str) -> Dict[str, Any]:
        path = f"/v2/orders/{order_id}"
        return await self.gateway.call(path, method="GET")

    async def tracking(self, order_id: str) -> Dict[str, Any]:
        params = {"orderId": order_id}
        return await self.gateway.call("/v2/orders/tracking", params)

    async def upload_image(self, file_name: str, file_bytes: bytes, content_type: str = "image/jpeg") -> Dict[str, Any]:
        files = {"file": (file_name, file_bytes, content_type)}
        return await self.gateway.call("/v2/images/upload", files=files, method="POST")
