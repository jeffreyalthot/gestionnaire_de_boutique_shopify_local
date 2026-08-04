from integrations.alibaba.base_method import AlibabaMethod


class TradeAddressList(AlibabaMethod):
    method = 'alibaba.trade.address.list.query'
    category = 'orders'
    mutating = False
