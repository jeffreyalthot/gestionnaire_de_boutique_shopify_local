from integrations.alibaba.base_method import AlibabaMethod


class TrackingGet(AlibabaMethod):
    method = 'alibaba.order.logistics.tracking.get'
    category = 'logistics'
    mutating = False
