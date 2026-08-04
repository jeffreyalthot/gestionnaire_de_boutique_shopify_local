class OrderEditService:
    IMMUTABLE={"id","shopify_order_id","created_at","customer_id"}
    def apply(self, order: dict[str,object], changes: dict[str,object], *, procurement_started: bool=False) -> dict[str,object]:
        if procurement_started and any(k in changes for k in ("lines","shipping_address")):
            raise ValueError("modification interdite après le début de l'approvisionnement")
        result=dict(order)
        for key,value in changes.items():
            if key in self.IMMUTABLE: raise ValueError(f"champ immuable: {key}")
            result[key]=value
        return result
