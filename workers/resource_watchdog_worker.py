from workers.specialized_worker import SpecializedWorker


class ResourceWatchdogWorker(SpecializedWorker):
    name = 'resourcewatchdog'
    queue = 'maintenance'
    accepted_task_types = ('resource_sample', 'resource_throttle', 'resource_recover')
