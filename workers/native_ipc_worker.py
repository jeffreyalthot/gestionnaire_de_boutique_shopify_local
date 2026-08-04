from workers.specialized_worker import SpecializedWorker


class NativeIpcWorker(SpecializedWorker):
    name = 'nativeipc'
    queue = 'default'
    accepted_task_types = ('native_command', 'native_snapshot', 'native_heartbeat')
