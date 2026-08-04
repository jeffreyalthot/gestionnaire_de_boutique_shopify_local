from sales_channels.base_adapter import ProductFeedAdapter
class GoogleMerchantAdapter(ProductFeedAdapter):
    channel="google_merchant"
    def map_product(self,p):
        out=super().map_product(p);out.update({"google_product_category":p.get("google_category",""),"gtin":p.get("barcode",""),"mpn":p.get("mpn",p.get("sku","")),"shipping_weight":p.get("weight","")});return out
