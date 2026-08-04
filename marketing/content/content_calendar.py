from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class ContentItem:
    publish_date: date
    channel: str
    topic: str
    status: str="planned"

class ContentCalendar:
    def __init__(self) -> None: self.items: list[ContentItem]=[]
    def add(self,item: ContentItem) -> None:
        if any(x.publish_date==item.publish_date and x.channel==item.channel for x in self.items): raise ValueError("créneau déjà occupé")
        self.items.append(item)
