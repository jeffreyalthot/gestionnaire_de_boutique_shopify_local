from integrations.alibaba.base_method import AlibabaMethod


class CategoryGet(AlibabaMethod):
    method = 'alibaba.icbu.category.get.new'
    category = 'products'
    mutating = False
