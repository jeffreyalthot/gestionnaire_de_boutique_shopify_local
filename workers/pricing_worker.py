from workers.base_worker import DelegatingWorker


class PricingWorker(DelegatingWorker):
    name = 'pricing'
    queue = 'pricing'
    method_candidates = ('reprice', 'price', 'execute')
