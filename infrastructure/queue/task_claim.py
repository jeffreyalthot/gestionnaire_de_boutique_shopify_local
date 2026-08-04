from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from infrastructure.queue.durable_queue import DurableQueue
from infrastructure.queue.task import QueueTask


@dataclass(frozen=True, slots=True)
class ClaimResult:
    task: QueueTask | None
    worker_id: str
    queues: tuple[str, ...]
    claimed_at: str

    @property
    def claimed(self) -> bool:
        return self.task is not None


def claim(queue: DurableQueue, worker_id: str, names: tuple[str, ...]) -> ClaimResult:
    worker = str(worker_id).strip()
    queue_names = tuple(dict.fromkeys(str(name).strip() for name in names if str(name).strip()))
    if not worker or len(worker) > 160:
        raise ValueError("worker_id_invalid")
    if not queue_names:
        raise ValueError("queue_names_required")
    return ClaimResult(queue.claim(worker, queue_names), worker, queue_names, datetime.now(timezone.utc).isoformat())


def claim_next(queue: DurableQueue, worker_id: str, names: tuple[str, ...]) -> QueueTask | None:
    return claim(queue, worker_id, names).task
