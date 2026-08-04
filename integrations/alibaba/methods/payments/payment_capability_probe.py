from integrations.alibaba.base_method import AlibabaMethod


class PaymentCapabilityProbe(AlibabaMethod):
    method = 'alibaba.dropshipping.order.pay'
    category = 'payments'
    mutating = True
