from workers.base_worker import DelegatingWorker


class AccountingWorker(DelegatingWorker):
    name = 'accounting'
    queue = 'accounting'
    method_candidates = ('account', 'post', 'execute')
