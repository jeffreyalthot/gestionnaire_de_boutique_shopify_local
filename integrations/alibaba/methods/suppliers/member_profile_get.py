from integrations.alibaba.base_method import AlibabaMethod


class MemberProfileGet(AlibabaMethod):
    method = 'alibaba.member.basicprofile.find'
    category = 'suppliers'
    mutating = False
