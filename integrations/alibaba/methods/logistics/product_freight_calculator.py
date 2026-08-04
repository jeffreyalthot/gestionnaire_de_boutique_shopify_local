from integrations.alibaba.base_method import AlibabaMethod


class ProductFreightCalculator(AlibabaMethod):
    method = 'alibaba.shipping.freight.calculate'
    category = 'logistics'
    mutating = True
