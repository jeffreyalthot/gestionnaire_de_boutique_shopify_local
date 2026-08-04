from integrations.alibaba.base_method import AlibabaMethod


class ProductGet(AlibabaMethod):
    method = 'alibaba.icbu.product.get'
    category = 'products'
    mutating = False
