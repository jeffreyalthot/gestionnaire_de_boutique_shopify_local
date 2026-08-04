from workers.base_worker import DelegatingWorker


class ReconciliationWorker(DelegatingWorker):
    name = 'reconciliation'
    queue = 'maintenance'
    method_candidates = ('reconcile', 'run', 'execute')
