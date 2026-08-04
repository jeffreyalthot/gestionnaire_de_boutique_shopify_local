from decimal import Decimal
from catalog.product_normalizer import ProductNormalizer
from catalog.variant_normalizer import normalize_variants
from catalog.title_generator import generate_title
from catalog.description_generator import generate_description
from catalog.image_pipeline import shopify_files
from catalog.quality_score import quality_score
from catalog.tag_generator import generate_tags
from pricing.pricing_engine import PricingEngine

class ProductImportPipeline:
    def __init__(self,pricing: PricingEngine,currency_converter) -> None:
        self.pricing=pricing; self.currency_converter=currency_converter; self.normalizer=ProductNormalizer()
    async def prepare(self,raw: dict[str,object],shipping_cost_source: Decimal) -> dict[str,object]:
        product=self.normalizer.normalize(raw)
        cost_cad=await self.currency_converter.convert(product["price"],str(product["currency"]),"CAD")
        shipping_cad=await self.currency_converter.convert(shipping_cost_source,str(product["currency"]),"CAD")
        decision=self.pricing.calculate(cost_cad,shipping_cad)
        title=generate_title(str(product["title"]))
        variants=normalize_variants(product["skus"],str(product["product_id"]))
        for variant in variants: variant["sale_price_cad"]=str(decision.sale_price_cad)
        attrs={"Catégorie":product.get("category_id",""),"Fournisseur":product.get("supplier",{}).get("name","") if isinstance(product.get("supplier"),dict) else ""}
        return {"supplier_product_id":product["product_id"],"title":title,
                "descriptionHtml":generate_description(title,attrs,str(product["description"])),
                "productType":str(product.get("category_id","")),"vendor":"Alibaba Supplier",
                "tags":generate_tags(title,str(product.get("category_id",""))),
                "files":shopify_files(product["images"],title),"variants":variants,
                "quality_score":quality_score(product),"landed_cost_cad":str(decision.landed_cost_cad),
                "sale_price_cad":str(decision.sale_price_cad),"margin_percent":str(decision.margin_percent)}
