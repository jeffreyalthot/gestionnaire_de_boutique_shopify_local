from workers.base_worker import DelegatingWorker


class ProductDiscoveryWorker(DelegatingWorker):
    name = 'product_discovery'
    queue = 'catalog'
    method_candidates = ('discover_products', 'discover', 'execute')
