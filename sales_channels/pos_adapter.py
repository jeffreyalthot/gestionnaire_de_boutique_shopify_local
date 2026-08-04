from __future__ import annotations
class POSAdapter:
    channel="pos"
    def inventory_payload(self,sku: str,quantity: int,location_id: str) -> dict[str,object]:
        sku=sku.strip();location_id=location_id.strip()
        if not sku or not location_id:raise ValueError("sku et location_id requis")
        return {"sku":sku,"quantity":max(0,int(quantity)),"location_id":location_id,"channel":self.channel}
    def reconcile(self,local: dict[str,int],remote: dict[str,int]) -> tuple[dict[str,object],...]:
        return tuple({"sku":sku,"local":int(local.get(sku,0)),"remote":int(remote.get(sku,0)),"delta":int(local.get(sku,0))-int(remote.get(sku,0))} for sku in sorted(set(local)|set(remote)) if int(local.get(sku,0))!=int(remote.get(sku,0)))
