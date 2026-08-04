from workers.specialized_worker import SpecializedWorker


class MaintenanceWorker(SpecializedWorker):
    name = 'maintenance'
    queue = 'maintenance'
    accepted_task_types = ('database_maintenance', 'cache_cleanup', 'retention_cleanup')
