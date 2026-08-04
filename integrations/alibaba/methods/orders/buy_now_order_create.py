from integrations.alibaba.base_method import AlibabaMethod


class BuyNowOrderCreate(AlibabaMethod):
    method = 'alibaba.buynow.order.create'
    category = 'orders'
    mutating = True
