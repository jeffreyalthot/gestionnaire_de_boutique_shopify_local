from integrations.alibaba.base_method import AlibabaMethod


class ShippingChannels(AlibabaMethod):
    method = 'alibaba.seller.order.shipping.channels'
    category = 'logistics'
    mutating = True
