from workers.base_worker import DelegatingWorker


class FulfillmentWorker(DelegatingWorker):
    name = 'fulfillment'
    queue = 'fulfillment'
    method_candidates = ('fulfill', 'sync', 'execute')
