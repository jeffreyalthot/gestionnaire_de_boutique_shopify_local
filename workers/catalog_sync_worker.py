from workers.base_worker import DelegatingWorker


class CatalogSyncWorker(DelegatingWorker):
    name = 'catalog_sync'
    queue = 'catalog'
    method_candidates = ('sync_catalog', 'sync', 'execute')
