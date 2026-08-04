from integrations.alibaba.base_method import AlibabaMethod


class SupplierList(AlibabaMethod):
    method = 'alibaba.procurement.mysupplier.list'
    category = 'suppliers'
    mutating = False
