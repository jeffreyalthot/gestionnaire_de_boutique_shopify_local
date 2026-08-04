from integrations.alibaba.base_method import AlibabaMethod


class SupplierItemsGet(AlibabaMethod):
    method = 'alibaba.procurement.supplier.items.get'
    category = 'suppliers'
    mutating = False
