from __future__ import annotations

from infrastructure.queue.durable_queue import DurableQueue


class RetryWorker:
    def __init__(self, queue: DurableQueue) -> None:
        self.queue = queue
        self.retried = 0
        self.failed = 0

    async def retry(self, task_id: str) -> bool:
        try:
            result = self.queue.retry_dead(str(task_id))
            self.retried += 1
            return bool(result is None or result)
        except Exception:
            self.failed += 1
            raise

    async def retry_many(self, task_ids: list[str], *, limit: int = 100) -> dict[str, object]:
        accepted: list[str] = []
        errors: dict[str, str] = {}
        for task_id in task_ids[: max(1, min(int(limit), 1000))]:
            try:
                if await self.retry(task_id):
                    accepted.append(task_id)
            except Exception as exc:
                errors[task_id] = f"{type(exc).__name__}: {exc}"[:500]
        return {"retried": accepted, "errors": errors, "ok": not errors}

    def stats(self) -> dict[str, int]:
        return {"retried": self.retried, "failed": self.failed}
