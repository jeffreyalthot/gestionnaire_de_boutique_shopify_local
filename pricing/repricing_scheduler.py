from infrastructure.queue.durable_queue import DurableQueue
from domain.value_objects.idempotency_key import build_idempotency_key
def schedule_reprice(queue: DurableQueue,product_id: str,delay_seconds: float=0) -> str:
    return queue.enqueue("reprice_product",{"product_id":product_id},
        build_idempotency_key("reprice",product_id),queue="pricing",delay_seconds=delay_seconds)
