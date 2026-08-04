from integrations.alibaba.base_method import AlibabaMethod


class ShippingSubmit(AlibabaMethod):
    method = 'alibaba.seller.order.shipping'
    category = 'logistics'
    mutating = True
