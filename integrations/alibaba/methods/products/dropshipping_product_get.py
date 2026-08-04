from integrations.alibaba.base_method import AlibabaMethod


class DropshippingProductGet(AlibabaMethod):
    method = 'alibaba.dropshipping.product.get'
    category = 'products'
    mutating = False
