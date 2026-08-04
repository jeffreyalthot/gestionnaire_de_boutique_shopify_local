from integrations.alibaba.base_method import AlibabaMethod


class ServiceChargeGet(AlibabaMethod):
    method = 'alibaba.trade.service.charge.get'
    category = 'payments'
    mutating = False
