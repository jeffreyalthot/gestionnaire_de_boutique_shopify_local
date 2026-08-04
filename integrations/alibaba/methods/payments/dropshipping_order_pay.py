from integrations.alibaba.base_method import AlibabaMethod


class DropshippingOrderPay(AlibabaMethod):
    method = 'alibaba.dropshipping.order.pay'
    category = 'payments'
    mutating = True
