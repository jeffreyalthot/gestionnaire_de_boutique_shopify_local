from workers.specialized_worker import SpecializedWorker


class CatalogMediaWorker(SpecializedWorker):
    name = 'catalogmedia'
    queue = 'media'
    accepted_task_types = ('media_download', 'media_validate', 'media_stage')
