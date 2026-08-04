from workers.specialized_worker import SpecializedWorker


class PaymentMonitorWorker(SpecializedWorker):
    name = 'paymentmonitor'
    queue = 'payments'
    accepted_task_types = ('payment_status', 'payment_reconcile', 'chargeback_monitor')
