from __future__ import annotations

from typing import Any

from infrastructure.queue.dead_letter_queue import dead_letters


class DeadLetterWorker:
    def __init__(self, db: Any, queue: Any | None = None, *, limit: int = 100) -> None:
        self.db = db
        self.queue = queue
        self.limit = max(1, min(int(limit), 1000))
        self.last_count = 0

    async def run_once(self) -> list[dict[str, object]]:
        rows = list(dead_letters(self.db))[: self.limit]
        self.last_count = len(rows)
        return rows

    async def requeue(self, task_id: str) -> bool:
        if self.queue is None:
            raise RuntimeError("File durable requise pour réessayer une lettre morte.")
        result = self.queue.retry_dead(str(task_id))
        return bool(result is None or result)

    def stats(self) -> dict[str, int]:
        return {"last_count": self.last_count, "limit": self.limit}
