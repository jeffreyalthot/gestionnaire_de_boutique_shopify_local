from integrations.alibaba.base_method import AlibabaMethod


class TmcTopicsGet(AlibabaMethod):
    method = 'taobao.tmc.user.topics.get'
    category = 'events'
    mutating = False
