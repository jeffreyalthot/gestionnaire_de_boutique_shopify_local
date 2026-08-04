from integrations.alibaba.base_method import AlibabaMethod


class DistributionProductQuery(AlibabaMethod):
    method = 'alibaba.icbu.distribution.product.query'
    category = 'products'
    mutating = False
