from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone

from infrastructure.queue.durable_queue import DurableQueue


@dataclass(frozen=True, slots=True)
class DelayedTaskReceipt:
    task_id: str
    available_at: str
    delay_seconds: float

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class DelayedQueue:
    def __init__(self, queue: DurableQueue) -> None:
        self.queue = queue

    def enqueue(self, task_type: str, payload: dict[str, object], key: str, seconds: float, *, priority: int = 0) -> DelayedTaskReceipt:
        delay = max(0.0, float(seconds))
        task_id = self.queue.enqueue(task_type, payload, key, delay_seconds=delay, priority=priority)
        return DelayedTaskReceipt(task_id, (datetime.now(timezone.utc) + timedelta(seconds=delay)).isoformat(), delay)


def enqueue_delayed(queue: DurableQueue, task_type: str, payload: dict[str, object], key: str, seconds: float) -> str:
    return DelayedQueue(queue).enqueue(task_type, payload, key, seconds).task_id
