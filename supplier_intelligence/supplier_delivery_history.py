class SupplierDeliveryHistory:
    def metrics(self,shipments: list[dict[str,object]]) -> dict[str,float]:
        total=len(shipments); on_time=sum(bool(x.get("on_time")) for x in shipments); delivered=sum(x.get("status")=="delivered" for x in shipments)
        return {"shipments":total,"delivery_rate":round(delivered/max(1,total),4),"on_time_rate":round(on_time/max(1,total),4)}
