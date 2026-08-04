from integrations.alibaba.base_method import AlibabaMethod


class TmcMessagesConfirm(AlibabaMethod):
    method = 'taobao.tmc.messages.confirm'
    category = 'events'
    mutating = True
