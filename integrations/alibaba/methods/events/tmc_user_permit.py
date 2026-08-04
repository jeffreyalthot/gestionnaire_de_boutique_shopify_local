from integrations.alibaba.base_method import AlibabaMethod


class TmcUserPermit(AlibabaMethod):
    method = 'taobao.tmc.user.permit'
    category = 'events'
    mutating = True
