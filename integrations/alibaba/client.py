from __future__ import annotations
import json
from typing import Any
from integrations.alibaba.gateway import AlibabaGateway

class AlibabaClient:
    def __init__(self,gateway: AlibabaGateway) -> None: self.gateway=gateway

    async def call(self,method: str,**params: Any) -> dict[str,Any]:
        return await self.gateway.call(method,params)

    async def search_distribution_products(self,keyword: str,page: int=1,page_size: int=50,
                                           category_id: str="") -> dict[str,Any]:
        return await self.call("alibaba.icbu.distribution.product.query",keyword=keyword,page=page,
                               page_size=page_size,category_id=category_id or None)

    async def distribution_product(self,product_id: str) -> dict[str,Any]:
        return await self.call("alibaba.icbu.distribution.product.get",product_id=product_id)

    async def dropshipping_product(self,product_id: str) -> dict[str,Any]:
        return await self.call("alibaba.dropshipping.product.get",product_id=product_id)

    async def product(self,product_id: str) -> dict[str,Any]:
        return await self.call("alibaba.icbu.product.get",product_id=product_id)

    async def product_inventory(self,product_id: str) -> dict[str,Any]:
        return await self.call("alibaba.icbu.product.inventory.get",product_id=product_id)

    async def sku_inventory(self,product_id: str) -> dict[str,Any]:
        return await self.call("alibaba.icbu.product.sku.inventory.get",product_id=product_id)

    async def calculate_product_freight(self,product_id: str,sku_id: str,quantity: int,
                                        country_code: str,postal_code: str) -> dict[str,Any]:
        return await self.call("alibaba.shipping.freight.calculate",product_id=product_id,sku_id=sku_id,
                               quantity=quantity,country_code=country_code,postal_code=postal_code)

    async def calculate_order_freight(self,items: list[dict[str,Any]],address: dict[str,Any]) -> dict[str,Any]:
        return await self.call("alibaba.order.freight.calculate",
                               items=json.dumps(items,separators=(",",":")),
                               address=json.dumps(address,separators=(",",":")))

    async def create_buy_now_order(self,items: list[dict[str,Any]],address: dict[str,Any],
                                   remark: str,idempotency_key: str) -> dict[str,Any]:
        return await self.call("alibaba.buynow.order.create",
                               items=json.dumps(items,separators=(",",":")),
                               receive_address=json.dumps(address,separators=(",",":")),
                               remark=remark,external_reference=idempotency_key)

    async def create_trade_assurance_order(self,items: list[dict[str,Any]],address: dict[str,Any],
                                           terms: dict[str,Any]) -> dict[str,Any]:
        return await self.call("alibaba.trade.order.create",
                               items=json.dumps(items,separators=(",",":")),
                               address=json.dumps(address,separators=(",",":")),
                               trade_terms=json.dumps(terms,separators=(",",":")))

    async def pay_dropshipping_order(self,order_id: str,payment_token_reference: str="") -> dict[str,Any]:
        params={"order_id":order_id}
        if payment_token_reference: params["payment_token_reference"]=payment_token_reference
        return await self.call("alibaba.dropshipping.order.pay",**params)

    async def payment_result(self,order_id: str) -> dict[str,Any]:
        return await self.call("alibaba.order.pay.result.query",order_id=order_id)

    async def order_funds(self,order_id: str) -> dict[str,Any]:
        return await self.call("alibaba.seller.order.fund.get",order_id=order_id)

    async def order(self,order_id: str) -> dict[str,Any]:
        return await self.call("alibaba.seller.order.get",order_id=order_id)

    async def orders(self,page: int=1,page_size: int=50,status: str="") -> dict[str,Any]:
        return await self.call("alibaba.seller.order.list",page=page,page_size=page_size,status=status or None)

    async def tracking(self,order_id: str) -> dict[str,Any]:
        return await self.call("alibaba.order.logistics.tracking.get",order_id=order_id)

    async def consume_events(self,quantity: int=100) -> dict[str,Any]:
        return await self.call("taobao.tmc.messages.consume",quantity=quantity)

    async def confirm_events(self,message_ids: list[str]) -> dict[str,Any]:
        return await self.call("taobao.tmc.messages.confirm",s_message_ids=",".join(message_ids))

    async def suppliers(self) -> dict[str,Any]:
        return await self.call("alibaba.procurement.mysupplier.list")

    async def supplier_items(self,supplier_id: str) -> dict[str,Any]:
        return await self.call("alibaba.procurement.supplier.items.get",supplier_id=supplier_id)

    async def supplier_profile(self, supplier_id: str) -> dict[str, Any]:
        return await self.call("alibaba.member.profile.get", supplier_id=supplier_id)

    async def supplier_credit_report(self, supplier_id: str) -> dict[str, Any]:
        return await self.call("alibaba.supplier.credit.report", supplier_id=supplier_id)

    async def photobank(self, page: int = 1, page_size: int = 50) -> dict[str, Any]:
        return await self.call("alibaba.photobank.list", page=page, page_size=page_size)

    async def categories(self, parent_id: str = "") -> dict[str, Any]:
        return await self.call("alibaba.icbu.category.get", parent_id=parent_id or None)

    async def category_attributes(self, category_id: str) -> dict[str, Any]:
        return await self.call("alibaba.icbu.category.attributes.get", category_id=category_id)

    async def shipping_channels(self, country_code: str) -> dict[str, Any]:
        return await self.call("alibaba.shipping.channels.get", country_code=country_code)
