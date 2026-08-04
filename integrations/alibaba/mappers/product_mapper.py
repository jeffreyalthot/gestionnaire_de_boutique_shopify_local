from decimal import Decimal
def _find(data: dict[str,object],*keys: str,default=None):
    for key in keys:
        if key in data and data[key] is not None: return data[key]
    return default
def map_alibaba_product(data: dict[str,object]) -> dict[str,object]:
    product_id=str(_find(data,"product_id","productId","id",default=""))
    title=str(_find(data,"subject","title","name",default=""))
    images=_find(data,"image_urls","images","imageList",default=[]) or []
    skus=_find(data,"sku_infos","skus","skuList",default=[]) or []
    supplier=_find(data,"supplier","company","seller",default={}) or {}
    return {"product_id":product_id,"title":title,"description":str(_find(data,"description","detail",default="")),
            "currency":str(_find(data,"currency","currencyCode",default="USD")),
            "price":Decimal(str(_find(data,"price","unitPrice","minPrice",default="0"))),
            "category_id":str(_find(data,"category_id","categoryId",default="")),
            "images":images if isinstance(images,list) else [images],
            "skus":skus if isinstance(skus,list) else [],
            "supplier":supplier if isinstance(supplier,dict) else {},"raw":data}
