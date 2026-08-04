from integrations.alibaba.base_method import AlibabaMethod


class SkuInventoryGet(AlibabaMethod):
    method = 'alibaba.icbu.product.sku.inventory.get'
    category = 'products'
    mutating = False
