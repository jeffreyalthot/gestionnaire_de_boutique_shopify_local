from workers.base_worker import DelegatingWorker


class CleanupWorker(DelegatingWorker):
    name = 'cleanup'
    queue = 'maintenance'
    method_candidates = ('cleanup', 'purge', 'execute')
