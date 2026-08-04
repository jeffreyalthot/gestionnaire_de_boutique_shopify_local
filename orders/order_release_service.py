from orders.order_repository import OrderRepository
from orders.order_timeline import OrderTimeline


class OrderReleaseService:
    def __init__(self, repository: OrderRepository, timeline: OrderTimeline) -> None: self.repository=repository; self.timeline=timeline
    def release(self, order_id: str, reason: str="approved") -> None:
        self.repository.update_status(order_id, procurement="pending")
        self.timeline.append(order_id,"order_released",status="pending",detail={"reason":reason})
