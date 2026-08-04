from integrations.alibaba.base_method import AlibabaMethod


class PhotobankList(AlibabaMethod):
    method = 'alibaba.icbu.photobank.list'
    category = 'products'
    mutating = False
