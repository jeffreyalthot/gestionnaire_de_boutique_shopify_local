from integrations.alibaba.base_method import AlibabaMethod


class TradeAddressSave(AlibabaMethod):
    method = 'alibaba.trade.address.form.save'
    category = 'orders'
    mutating = True
