from integrations.alibaba.base_method import AlibabaMethod


class SellerOrderList(AlibabaMethod):
    method = 'alibaba.seller.order.list'
    category = 'orders'
    mutating = False
