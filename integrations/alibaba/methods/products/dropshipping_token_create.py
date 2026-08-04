from integrations.alibaba.base_method import AlibabaMethod


class DropshippingTokenCreate(AlibabaMethod):
    method = 'alibaba.dropshipping.token.create'
    category = 'products'
    mutating = True
