from integrations.alibaba.gateway import AlibabaGateway
CAPABILITY_METHODS={
"product_search":"alibaba.icbu.distribution.product.query",
"product_detail":"alibaba.dropshipping.product.get",
"inventory":"alibaba.icbu.product.sku.inventory.get",
"freight":"alibaba.shipping.freight.calculate",
"order_create":"alibaba.buynow.order.create",
"payment":"alibaba.dropshipping.order.pay",
"tracking":"alibaba.order.logistics.tracking.get",
"events":"taobao.tmc.messages.consume",
}
class AlibabaPermissionProbe:
    def __init__(self,gateway: AlibabaGateway) -> None: self.gateway=gateway
    async def probe_read_capabilities(self) -> dict[str,dict[str,object]]:
        probes={
          "product_search":("alibaba.icbu.distribution.product.query",{"keyword":"test","page":1,"page_size":1}),
          "orders":("alibaba.seller.order.list",{"page":1,"page_size":1}),
          "suppliers":("alibaba.procurement.mysupplier.list",{}),
          "events":("taobao.tmc.queue.get",{}),
        }
        result={}
        for name,(method,params) in probes.items():
            try:
                await self.gateway.call(method,params)
                result[name]={"available":True,"error":""}
            except Exception as exc:
                result[name]={"available":False,"error":str(exc)}
        return result
