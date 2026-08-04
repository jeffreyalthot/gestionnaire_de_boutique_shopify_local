from integrations.alibaba.base_method import AlibabaMethod


class LogisticsCountryCostStatus(AlibabaMethod):
    method = 'alibaba.icbu.product.logistics.country.getcoststatus'
    category = 'products'
    mutating = False
