from integrations.alibaba.base_method import AlibabaMethod


class OrderLogisticsGet(AlibabaMethod):
    method = 'alibaba.seller.order.logistics.get'
    category = 'logistics'
    mutating = False
