from __future__ import annotations
from dataclasses import asdict,dataclass
from domain.value_objects.idempotency_key import build_idempotency_key
from infrastructure.queue.durable_queue import DurableQueue

@dataclass(frozen=True,slots=True)
class StockUpdateReceipt:
    task_id: str
    product_id: str
    reason: str
    priority: int
    idempotency_key: str
    def as_dict(self):return asdict(self)

class StockUpdateScheduler:
    def __init__(self,queue: DurableQueue) -> None:self.queue=queue
    def schedule(self,product_id: str,*,reason: str="periodic",priority: int=100,delay_seconds: float=0,force_key_suffix: str="") -> StockUpdateReceipt:
        product_id=str(product_id).strip()
        if not product_id:raise ValueError("product_id requis")
        key=build_idempotency_key("inventory",product_id,reason,force_key_suffix);task=self.queue.enqueue("sync_inventory",{"product_id":product_id,"reason":reason},key,queue="inventory",priority=priority,delay_seconds=delay_seconds);return StockUpdateReceipt(task,product_id,reason,priority,key)

def schedule_stock_update(queue: DurableQueue,product_id: str) -> str:return StockUpdateScheduler(queue).schedule(product_id).task_id
