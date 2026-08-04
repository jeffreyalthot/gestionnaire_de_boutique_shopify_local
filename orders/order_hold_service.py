from orders.order_repository import OrderRepository
from orders.order_timeline import OrderTimeline


class OrderHoldService:
    def __init__(self, repository: OrderRepository, timeline: OrderTimeline) -> None: self.repository=repository; self.timeline=timeline
    def hold(self, order_id: str, reason: str) -> None:
        self.repository.update_status(order_id, procurement="held")
        self.timeline.append(order_id,"order_held",status="held",detail={"reason":reason})
