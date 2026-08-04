from sales_channels.base_adapter import ProductFeedAdapter
class TikTokShopAdapter(ProductFeedAdapter):
    channel="tiktok_shop"
    max_title=120
    def map_product(self,p):
        out=super().map_product(p);out.update({"seller_sku":p.get("sku",out["id"]),"category_id":p.get("tiktok_category_id",""),"package_weight":p.get("weight",0),"warehouse_quantity":max(0,int(p.get("stock",0) or 0))});return out
