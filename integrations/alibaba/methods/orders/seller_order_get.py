from integrations.alibaba.base_method import AlibabaMethod


class SellerOrderGet(AlibabaMethod):
    method = 'alibaba.seller.order.get'
    category = 'orders'
    mutating = False
