from infrastructure.database.engine import Database,utcnow
from integrations.alibaba.client import AlibabaClient
from integrations.alibaba.mappers.tracking_mapper import map_tracking
from integrations.shopify.client import ShopifyClient
class TrackingSync:
    def __init__(self,db: Database,alibaba: AlibabaClient,shopify: ShopifyClient) -> None:
        self.db=db; self.alibaba=alibaba; self.shopify=shopify
    async def sync(self,shipment: dict[str,object]) -> dict[str,object]:
        tracking=map_tracking(await self.alibaba.tracking(str(shipment["supplier_order_id"])))
        self.db.execute("UPDATE shipments SET carrier=?,tracking_number=?,tracking_url=?,status=?,events_json=?,updated_at=? WHERE id=?",
                        (tracking["carrier"],tracking["tracking_number"],tracking["tracking_url"],tracking["status"],
                         __import__("json").dumps(tracking["events"],ensure_ascii=False,default=str),utcnow(),shipment["id"]))
        order=self.db.query_one("SELECT * FROM orders WHERE id=?",(shipment["order_id"],))
        if order and tracking["tracking_number"] and not self.shopify.transport.settings.app_dry_run:
            fulfillments=await self.shopify.fulfillment_orders(str(order["shopify_order_id"]))
            if fulfillments:
                await self.shopify.create_fulfillment(fulfillments[0]["id"],
                    {"company":tracking["carrier"],"number":tracking["tracking_number"],"url":tracking["tracking_url"]})
        return tracking
