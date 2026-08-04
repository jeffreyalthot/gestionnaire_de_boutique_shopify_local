from workers.base_worker import DelegatingWorker


class PaymentWorker(DelegatingWorker):
    name = 'payment'
    queue = 'payments'
    method_candidates = ('pay', 'process_payment', 'execute')
