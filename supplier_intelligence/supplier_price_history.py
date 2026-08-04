from pricing.price_history import PriceHistory


class SupplierPriceHistory(PriceHistory):
    def record_offer(self,supplier_id: str,sku: str,price_cad: float,metadata=None) -> str: return self.record("supplier_offer",f"{supplier_id}:{sku}",price_cad=price_cad,source=supplier_id,metadata=metadata)
