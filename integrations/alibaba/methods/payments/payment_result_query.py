from integrations.alibaba.base_method import AlibabaMethod


class PaymentResultQuery(AlibabaMethod):
    method = 'alibaba.order.pay.result.query'
    category = 'payments'
    mutating = False
