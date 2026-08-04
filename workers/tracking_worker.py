from workers.base_worker import DelegatingWorker


class TrackingWorker(DelegatingWorker):
    name = 'tracking'
    queue = 'fulfillment'
    method_candidates = ('track', 'sync_tracking', 'execute')
