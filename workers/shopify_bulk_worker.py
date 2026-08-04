from workers.specialized_worker import SpecializedWorker


class ShopifyBulkWorker(SpecializedWorker):
    name = 'shopifybulk'
    queue = 'shopify'
    accepted_task_types = ('shopify_bulk_query', 'shopify_bulk_mutation', 'shopify_bulk_download')
