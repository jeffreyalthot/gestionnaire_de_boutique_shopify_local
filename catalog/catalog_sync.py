from infrastructure.queue.durable_queue import DurableQueue
from domain.value_objects.idempotency_key import build_idempotency_key
class CatalogSync:
    def __init__(self,queue: DurableQueue) -> None: self.queue=queue
    def schedule(self,product_id: str) -> str:
        return self.queue.enqueue("sync_product",{"product_id":product_id},
            build_idempotency_key("sync-product",product_id),queue="catalog")
