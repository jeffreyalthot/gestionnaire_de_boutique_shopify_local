from orders.order_timeline import OrderTimeline


class OrderNoteService:
    def __init__(self, timeline: OrderTimeline) -> None: self.timeline=timeline
    def add(self, order_id: str, note: str, actor: str="system") -> str:
        cleaned=" ".join(note.split())[:1000]
        if not cleaned: raise ValueError("note vide")
        return self.timeline.append(order_id,"note",detail={"actor":actor,"note":cleaned})
