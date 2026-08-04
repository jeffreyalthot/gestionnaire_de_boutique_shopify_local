from integrations.alibaba.base_method import AlibabaMethod


class CategoryAttributesGet(AlibabaMethod):
    method = 'alibaba.icbu.category.attribute.get'
    category = 'products'
    mutating = False
