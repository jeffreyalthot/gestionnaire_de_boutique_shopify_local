from workers.base_worker import DelegatingWorker


class AiTrainingWorker(DelegatingWorker):
    name = 'ai_training'
    queue = 'ai'
    method_candidates = ('train', 'fit', 'execute')
