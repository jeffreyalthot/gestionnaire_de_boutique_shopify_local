from workers.specialized_worker import SpecializedWorker


class ExceptionWorker(SpecializedWorker):
    name = 'exception'
    queue = 'maintenance'
    accepted_task_types = ('exception_retry', 'exception_compensate', 'stuck_operation_recovery')
