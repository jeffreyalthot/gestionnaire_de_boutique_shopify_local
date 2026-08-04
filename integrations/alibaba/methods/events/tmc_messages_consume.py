from integrations.alibaba.base_method import AlibabaMethod


class TmcMessagesConsume(AlibabaMethod):
    method = 'taobao.tmc.messages.consume'
    category = 'events'
    mutating = False
