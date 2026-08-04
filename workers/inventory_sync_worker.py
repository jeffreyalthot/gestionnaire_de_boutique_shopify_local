from workers.base_worker import DelegatingWorker


class InventorySyncWorker(DelegatingWorker):
    name = 'inventory_sync'
    queue = 'inventory'
    method_candidates = ('sync_inventory', 'sync', 'execute')
