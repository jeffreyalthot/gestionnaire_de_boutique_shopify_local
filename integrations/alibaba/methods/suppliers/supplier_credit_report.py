from integrations.alibaba.base_method import AlibabaMethod


class SupplierCreditReport(AlibabaMethod):
    method = 'alibaba.seller.assurance.credit.card'
    category = 'suppliers'
    mutating = False
