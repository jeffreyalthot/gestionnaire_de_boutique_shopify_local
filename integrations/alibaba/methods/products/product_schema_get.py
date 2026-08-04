from integrations.alibaba.base_method import AlibabaMethod


class ProductSchemaGet(AlibabaMethod):
    method = 'alibaba.icbu.product.schema.get'
    category = 'products'
    mutating = False
