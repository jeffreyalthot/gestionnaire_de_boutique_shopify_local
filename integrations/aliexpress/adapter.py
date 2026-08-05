"""AliExpress adapter exposing the same surface as the existing AlibabaClient.

This allows the rest of the application to keep calling the Alibaba-style
methods while the adapter translates them to AliExpress REST calls where
possible. Not all Alibaba RPC methods have direct equivalents in AliExpress;
methods without a clear mapping raise NotImplementedError so they can be
implemented on demand.
"""

from __future__ import annotations

from typing import Any

from integrations.aliexpress.client import AliExpressClient


class AliExpressAdapter:
    """Adapter providing AlibabaClient-like methods backed by AliExpress.

    Only a subset of methods are implemented (those commonly used for
    dropshipping: product search, get product, inventory, orders, tracking).
    Other methods raise NotImplementedError and should be added as needed.
    """

    def __init__(self, client: AliExpressClient) -> None:
        self.client = client

    async def call(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Compatibility stub for the low-level call signature.

        AliExpress uses REST endpoints; this stub attempts to route a few
        known Alibaba method names to AliExpress equivalents. For unknown
        methods it raises NotImplementedError.
        """
        params = params or {}
        method = method or ""
        # Simple routing for a few method names
        if method == "alibaba.icbu.distribution.product.query":
            keyword = params.get("keyword") or ""
            page = int(params.get("page") or 1)
            page_size = int(params.get("page_size") or params.get("pageSize") or 50)
            return await self.search_distribution_products(keyword, page=page, page_size=page_size)
        raise NotImplementedError(f"Raw call({method}) is not implemented for AliExpress adapter")

    async def search_distribution_products(self, keyword: str, page: int = 1, page_size: int = 50,
                                           category_id: str = "") -> dict[str, Any]:
        return await self.client.search_products(keyword, page=page, page_size=page_size)

    async def distribution_product(self, product_id: str) -> dict[str, Any]:
        return await self.client.get_product(product_id)

    async def dropshipping_product(self, product_id: str) -> dict[str, Any]:
        return await self.client.get_product(product_id)

    async def product(self, product_id: str) -> dict[str, Any]:
        return await self.client.get_product(product_id)

    async def product_inventory(self, product_id: str) -> dict[str, Any]:
        return await self.client.get_product_inventory(product_id)

    async def sku_inventory(self, product_id: str) -> dict[str, Any]:
        # AliExpress doesn't expose the exact same SKU inventory RPC; use inventory endpoint
        return await self.client.get_product_inventory(product_id)

    async def calculate_product_freight(self, product_id: str, sku_id: str, quantity: int,
                                        country_code: str, postal_code: str) -> dict[str, Any]:
        raise NotImplementedError("calculate_product_freight not implemented for AliExpress yet")

    async def calculate_order_freight(self, items: list[dict[str, Any]], address: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError("calculate_order_freight not implemented for AliExpress yet")

    async def create_buy_now_order(self, items: list[dict[str, Any]], address: dict[str, Any],
                                   remark: str, idempotency_key: str) -> dict[str, Any]:
        payload = {
            "items": items,
            "receive_address": address,
            "remark": remark,
            "external_reference": idempotency_key,
        }
        return await self.client.create_order(payload)

    async def create_trade_assurance_order(self, items: list[dict[str, Any]], address: dict[str, Any],
                                           terms: dict[str, Any]) -> dict[str, Any]:
        payload = {"items": items, "address": address, "trade_terms": terms}
        return await self.client.create_order(payload)

    async def pay_dropshipping_order(self, order_id: str, payment_token_reference: str = "") -> dict[str, Any]:
        # AliExpress payment flow differs; raise for now
        raise NotImplementedError("pay_dropshipping_order not implemented for AliExpress yet")

    async def payment_result(self, order_id: str) -> dict[str, Any]:
        raise NotImplementedError("payment_result not implemented for AliExpress yet")

    async def order_funds(self, order_id: str) -> dict[str, Any]:
        raise NotImplementedError("order_funds not implemented for AliExpress yet")

    async def order(self, order_id: str) -> dict[str, Any]:
        return await self.client.get_order(order_id)

    async def orders(self, page: int = 1, page_size: int = 50, status: str = "") -> dict[str, Any]:
        return await self.client.list_orders(page=page, page_size=page_size, status=status or None)

    async def tracking(self, order_id: str) -> dict[str, Any]:
        return await self.client.tracking(order_id)

    async def consume_events(self, quantity: int = 100) -> dict[str, Any]:
        raise NotImplementedError("consume_events (TMC) not available on AliExpress Open Platform")

    async def confirm_events(self, message_ids: list[str]) -> dict[str, Any]:
        raise NotImplementedError("confirm_events (TMC) not available on AliExpress Open Platform")

    async def suppliers(self) -> dict[str, Any]:
        raise NotImplementedError("suppliers not implemented for AliExpress yet")

    async def supplier_items(self, supplier_id: str) -> dict[str, Any]:
        raise NotImplementedError("supplier_items not implemented for AliExpress yet")

    async def supplier_profile(self, supplier_id: str) -> dict[str, Any]:
        raise NotImplementedError("supplier_profile not implemented for AliExpress yet")

    async def supplier_credit_report(self, supplier_id: str) -> dict[str, Any]:
        raise NotImplementedError("supplier_credit_report not implemented for AliExpress yet")

    async def photobank(self, page: int = 1, page_size: int = 50) -> dict[str, Any]:
        raise NotImplementedError("photobank not implemented for AliExpress yet")

    async def categories(self, parent_id: str = "") -> dict[str, Any]:
        # AliExpress provides /v2/categories
        # We'll map to a simple GET /v2/categories with optional parentId
        params: dict[str, Any] = {}
        if parent_id:
            params["parentId"] = parent_id
        return await self.client.gateway.request("/v2/categories", method="GET", params=params)

    async def category_attributes(self, category_id: str) -> dict[str, Any]:
        raise NotImplementedError("category_attributes not implemented for AliExpress yet")

    async def shipping_channels(self, country_code: str) -> dict[str, Any]:
        return await self.client.gateway.request("/v2/logistics/companies", method="GET", params={"countryCode": country_code})
