from integrations.alibaba.base_method import AlibabaMethod


class InventoryGet(AlibabaMethod):
    method = 'alibaba.icbu.product.inventory.get'
    category = 'products'
    mutating = False
