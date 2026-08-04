from sales_channels.base_adapter import ProductFeedAdapter
class MetaCatalogAdapter(ProductFeedAdapter):
    channel="meta_catalog"
    max_title=100
    def map_product(self,p):
        out=super().map_product(p);out.update({"retailer_id":out["id"],"inventory":max(0,int(p.get("stock",0) or 0)),"sale_price":self._money(p.get("compare_at_price_cad") or p.get("price_cad",0))});return out
