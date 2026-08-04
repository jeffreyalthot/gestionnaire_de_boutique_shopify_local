from integrations.alibaba.base_method import AlibabaMethod


class IntentionOrderSave(AlibabaMethod):
    method = 'alibaba.intention.order.save'
    category = 'orders'
    mutating = True
