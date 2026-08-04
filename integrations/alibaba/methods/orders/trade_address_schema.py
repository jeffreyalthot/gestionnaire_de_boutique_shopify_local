from integrations.alibaba.base_method import AlibabaMethod


class TradeAddressSchema(AlibabaMethod):
    method = 'alibaba.trade.address.schema.query'
    category = 'orders'
    mutating = False
