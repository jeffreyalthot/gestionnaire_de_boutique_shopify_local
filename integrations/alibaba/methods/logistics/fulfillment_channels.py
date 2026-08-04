from integrations.alibaba.base_method import AlibabaMethod


class FulfillmentChannels(AlibabaMethod):
    method = 'alibaba.trade.fulfillment.channel.get'
    category = 'logistics'
    mutating = False
