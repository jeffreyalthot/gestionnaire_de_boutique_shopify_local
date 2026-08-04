from integrations.alibaba.base_method import AlibabaMethod


class OrderFundsGet(AlibabaMethod):
    method = 'alibaba.seller.order.fund.get'
    category = 'payments'
    mutating = False
