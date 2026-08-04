from integrations.alibaba.base_method import AlibabaMethod


class ProductList(AlibabaMethod):
    method = 'alibaba.icbu.product.list'
    category = 'products'
    mutating = False
