from workers.specialized_worker import SpecializedWorker


class CatalogResearchWorker(SpecializedWorker):
    name = 'catalogresearch'
    queue = 'catalog'
    accepted_task_types = ('catalog_discovery', 'catalog_score', 'catalog_shortlist')
