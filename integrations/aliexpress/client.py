"""AliExpress integration - client implementation (full endpoint coverage).

This client exposes methods for the v2 endpoints documented for the
AliExpress Open Platform. Methods are thin wrappers that delegate to the
AliExpressGateway which handles HTTP, retries, rate limiting and error mapping.

Each method returns the raw parsed JSON payload from the gateway; callers may
map the payload to internal domain objects as needed.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from config.settings import get_settings
from integrations.aliexpress.gateway import AliExpressGateway


class AliExpressClient:
    def __init__(self, gateway: Optional[AliExpressGateway] = None) -> None:
        self.settings = get_settings()
        self.gateway = gateway or AliExpressGateway(self.settings)

    # -------------------- Authentication / Tokens --------------------
    async def create_token(self, code: str) -> Dict[str, Any]:
        return await self.gateway.call("/authorization", body={"code": code}, method="POST", session_required=False)

    async def create_token_via_oauth(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self.gateway.call("/token/create", body=payload, method="POST", session_required=False)

    async def refresh_token(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self.gateway.call("/token/refresh", body=payload, method="POST", session_required=False)

    async def revoke_token(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self.gateway.call("/token/revoke", body=payload, method="POST", session_required=False)

    # -------------------- Products --------------------
    async def get_products(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/products", params=params)

    async def get_product(self, product_id: str) -> Dict[str, Any]:
        return await self.gateway.call(f"/v2/products/{product_id}", method="GET")

    async def search_products(self, query: str, page: int = 1, page_size: int = 50) -> Dict[str, Any]:
        params = {"query": query, "page": page, "page_size": page_size}
        return await self.gateway.call("/v2/products/search", params=params)

    async def get_product_categories(self) -> Dict[str, Any]:
        return await self.gateway.call("/v2/products/categories", method="GET")

    async def get_products_by_category(self, category_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        path = f"/v2/products/category/{category_id}"
        return await self.gateway.call(path, params=params)

    async def get_product_images(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/products/images", params=params)

    async def get_product_inventory(self, product_id: str) -> Dict[str, Any]:
        params = {"productId": product_id}
        return await self.gateway.call("/v2/products/inventory", params=params)

    async def get_product_prices(self, product_id: str) -> Dict[str, Any]:
        params = {"productId": product_id}
        return await self.gateway.call("/v2/products/prices", params=params)

    async def get_product_shipping(self, product_id: str) -> Dict[str, Any]:
        params = {"productId": product_id}
        return await self.gateway.call("/v2/products/shipping", params=params)

    async def get_product_description(self, product_id: str) -> Dict[str, Any]:
        params = {"productId": product_id}
        return await self.gateway.call("/v2/products/description", params=params)

    async def get_product_attributes(self, product_id: str) -> Dict[str, Any]:
        params = {"productId": product_id}
        return await self.gateway.call("/v2/products/attributes", params=params)

    async def get_product_reviews(self, product_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        path = f"/v2/products/reviews"
        q = {**(params or {}), "productId": product_id}
        return await self.gateway.call(path, params=q)

    # -------------------- Orders --------------------
    async def list_orders(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/orders", params=params)

    async def get_order(self, order_id: str) -> Dict[str, Any]:
        return await self.gateway.call(f"/v2/orders/{order_id}")

    async def create_order(self, order_payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self.gateway.call("/v2/orders", body=order_payload, method="POST")

    async def cancel_order(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self.gateway.call("/v2/orders/cancel", body=payload, method="POST")

    async def confirm_order(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self.gateway.call("/v2/orders/confirm", body=payload, method="POST")

    async def get_order_status(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/orders/status", params=params)

    async def get_order_tracking(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/orders/tracking", params=params)

    # -------------------- Logistics / Shipping --------------------
    async def get_logistics(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/logistics", params=params)

    async def get_logistics_companies(self) -> Dict[str, Any]:
        return await self.gateway.call("/v2/logistics/companies")

    async def get_logistics_tracking(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/logistics/tracking", params=params)

    async def create_logistics(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self.gateway.call("/v2/logistics/create", body=payload, method="POST")

    async def update_logistics(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self.gateway.call("/v2/logistics/update", body=payload, method="POST")

    # -------------------- Payments --------------------
    async def get_payment_status(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/payment/status", params=params)

    async def get_payment_history(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/payment/history", params=params)

    # -------------------- Customers --------------------
    async def list_customers(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/customers", params=params)

    async def get_customer(self, customer_id: str) -> Dict[str, Any]:
        return await self.gateway.call(f"/v2/customers/{customer_id}")

    # -------------------- Images --------------------
    async def upload_image(self, file_name: str, file_bytes: bytes, content_type: str = "image/jpeg") -> Dict[str, Any]:
        files = {"file": (file_name, file_bytes, content_type)}
        return await self.gateway.call("/v2/images/upload", files=files, method="POST")

    async def get_image(self, image_id: str) -> Dict[str, Any]:
        return await self.gateway.call(f"/v2/images/{image_id}")

    async def delete_image(self, image_id: str) -> Dict[str, Any]:
        return await self.gateway.call(f"/v2/images/{image_id}", method="DELETE")

    # -------------------- Categories --------------------
    async def get_categories(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/categories", params=params)

    async def get_category_tree(self) -> Dict[str, Any]:
        return await self.gateway.call("/v2/categories/tree")

    async def get_category(self, category_id: str) -> Dict[str, Any]:
        return await self.gateway.call(f"/v2/categories/{category_id}")

    # -------------------- Attributes --------------------
    async def get_attributes(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/attributes", params=params)

    async def get_attributes_for_category(self, category_id: str) -> Dict[str, Any]:
        return await self.gateway.call(f"/v2/attributes/{category_id}")

    # -------------------- Inventory / Stock --------------------
    async def get_inventory(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/inventory", params=params)

    async def get_inventory_for_product(self, product_id: str) -> Dict[str, Any]:
        return await self.gateway.call(f"/v2/inventory/{product_id}")

    async def update_inventory(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self.gateway.call("/v2/inventory/update", body=payload, method="POST")

    # -------------------- Pricing --------------------
    async def get_pricing(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/pricing", params=params)

    async def update_pricing(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self.gateway.call("/v2/pricing/update", body=payload, method="POST")

    # -------------------- Coupons --------------------
    async def get_coupons(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/coupons", params=params)

    async def apply_coupon(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self.gateway.call("/v2/coupons/apply", body=payload, method="POST")

    # -------------------- Messages --------------------
    async def list_messages(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/messages", params=params)

    async def send_message(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self.gateway.call("/v2/messages/send", body=payload, method="POST")

    # -------------------- Refunds --------------------
    async def list_refunds(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/refunds", params=params)

    async def create_refund(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self.gateway.call("/v2/refunds/create", body=payload, method="POST")

    async def update_refund(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self.gateway.call("/v2/refunds/update", body=payload, method="POST")

    # -------------------- Affiliate / Dropshipping Affiliate --------------------
    async def affiliate_products(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/affiliate/products", params=params)

    async def affiliate_categories(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/affiliate/categories", params=params)

    async def affiliate_hotproducts(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/affiliate/hotproducts", params=params)

    async def affiliate_search(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/affiliate/search", params=params)

    async def affiliate_links(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/affiliate/links", params=params)

    async def create_affiliate_link(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self.gateway.call("/v2/affiliate/link/create", body=payload, method="POST")

    async def affiliate_orders(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/affiliate/orders", params=params)

    async def affiliate_commission(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/affiliate/commission", params=params)

    async def affiliate_report(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/affiliate/report", params=params)

    # -------------------- Shipping --------------------
    async def get_shipping_methods(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/shipping/methods", params=params)

    async def get_shipping_cost(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/shipping/cost", params=params)

    async def get_shipping_time(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/shipping/time", params=params)

    # -------------------- Reviews / Ratings --------------------
    async def get_reviews(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/reviews", params=params)

    async def get_reviews_for_product(self, product_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        p = {**(params or {}), "productId": product_id}
        return await self.gateway.call("/v2/reviews/{productId}", params=p)

    # -------------------- Synchronisation --------------------
    async def sync_products(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/sync/products", params=params)

    async def sync_orders(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/sync/orders", params=params)

    async def sync_inventory(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/sync/inventory", params=params)

    async def sync_pricing(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/sync/pricing", params=params)

    # -------------------- Notifications / Webhooks --------------------
    async def register_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self.gateway.call("/v2/webhooks/register", body=payload, method="POST")

    async def delete_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self.gateway.call("/v2/webhooks/delete", body=payload, method="POST")

    async def list_webhooks(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/webhooks", params=params)

    # -------------------- Statistics --------------------
    async def get_statistics(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/statistics", params=params)

    async def get_statistics_orders(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/statistics/orders", params=params)

    async def get_statistics_products(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/statistics/products", params=params)

    async def get_statistics_sales(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.gateway.call("/v2/statistics/sales", params=params)
