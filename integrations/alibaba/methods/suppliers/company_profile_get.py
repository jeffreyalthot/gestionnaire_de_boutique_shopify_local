from integrations.alibaba.base_method import AlibabaMethod


class CompanyProfileGet(AlibabaMethod):
    method = 'alibaba.buyer.companyprofile.find'
    category = 'suppliers'
    mutating = False
