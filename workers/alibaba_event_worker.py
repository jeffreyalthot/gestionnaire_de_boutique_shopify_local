from workers.base_worker import DelegatingWorker


class AlibabaEventWorker(DelegatingWorker):
    name = 'alibaba_event'
    queue = 'alibaba'
    method_candidates = ('alibaba_event', 'consume', 'execute')
