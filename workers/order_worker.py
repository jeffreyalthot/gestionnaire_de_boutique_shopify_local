from workers.base_worker import DelegatingWorker


class OrderWorker(DelegatingWorker):
    name = 'order'
    queue = 'orders'
    method_candidates = ('process_order', 'process', 'execute')
