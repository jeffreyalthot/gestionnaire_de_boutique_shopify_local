from __future__ import annotations

from dataclasses import asdict, dataclass

from infrastructure.queue.durable_queue import DurableQueue


@dataclass(frozen=True, slots=True)
class PriorityTaskReceipt:
    task_id: str
    priority: int
    queue_class: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class PriorityQueue:
    LEVELS = {"low": -5, "normal": 0, "high": 5, "urgent": 10, "critical": 20}

    def __init__(self, queue: DurableQueue) -> None:
        self.queue = queue

    def enqueue(self, task_type: str, payload: dict[str, object], key: str, *, priority: int | str = 0) -> PriorityTaskReceipt:
        value = self.LEVELS.get(priority, 0) if isinstance(priority, str) else max(-100, min(100, int(priority)))
        task_id = self.queue.enqueue(task_type, payload, key, priority=value)
        category = next((name for name, level in sorted(self.LEVELS.items(), key=lambda item: item[1], reverse=True) if value >= level), "low")
        return PriorityTaskReceipt(task_id, value, category)


def enqueue_urgent(queue: DurableQueue, task_type: str, payload: dict[str, object], key: str) -> str:
    return PriorityQueue(queue).enqueue(task_type, payload, key, priority="urgent").task_id
