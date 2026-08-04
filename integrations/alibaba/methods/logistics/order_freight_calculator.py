from integrations.alibaba.base_method import AlibabaMethod


class OrderFreightCalculator(AlibabaMethod):
    method = 'alibaba.order.freight.calculate'
    category = 'logistics'
    mutating = False
