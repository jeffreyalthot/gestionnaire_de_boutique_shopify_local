from __future__ import annotations
class ShopAppAdapter:
    channel="shop_app"
    def publication_input(self,product_id: str,published: bool=True) -> dict[str,object]:
        if not str(product_id).startswith("gid://shopify/Product/"):raise ValueError("ID produit Shopify invalide")
        return {"productId":product_id,"published":bool(published),"channel":self.channel}
    def eligibility(self,product: dict[str,object]) -> dict[str,object]:
        issues=[]
        if product.get("restricted"):issues.append("restricted_product")
        if float(product.get("price_cad",0) or 0)<=0:issues.append("invalid_price")
        if not product.get("image_url"):issues.append("missing_image")
        return {"eligible":not issues,"issues":tuple(issues)}
