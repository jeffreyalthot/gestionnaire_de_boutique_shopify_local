from integrations.alibaba.base_method import AlibabaMethod


class OrderPaymentResult(AlibabaMethod):
    method = 'alibaba.order.pay.result.query'
    category = 'orders'
    mutating = False
