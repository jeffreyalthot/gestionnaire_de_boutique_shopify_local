from integrations.alibaba.base_method import AlibabaMethod


class TmcQueueStatus(AlibabaMethod):
    method = 'taobao.tmc.queue.get'
    category = 'events'
    mutating = False
