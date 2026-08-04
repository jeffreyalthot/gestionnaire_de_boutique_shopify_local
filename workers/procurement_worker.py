from workers.base_worker import DelegatingWorker


class ProcurementWorker(DelegatingWorker):
    name = 'procurement'
    queue = 'procurement'
    method_candidates = ('procure', 'purchase', 'execute')
