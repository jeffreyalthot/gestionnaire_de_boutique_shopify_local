from integrations.alibaba.base_method import AlibabaMethod


class TradeAssuranceOrderCreate(AlibabaMethod):
    method = 'alibaba.trade.order.create'
    category = 'orders'
    mutating = True
