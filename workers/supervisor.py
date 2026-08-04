from __future__ import annotations

import asyncio
import logging
from uuid import uuid4

from automation.exceptions.retry_decider import RetryDecider
from workers.worker_context import WorkerContext

logger = logging.getLogger(__name__)


class WorkerSupervisor:
    def __init__(self, context: WorkerContext, handlers: dict[str, object],
                 queues: tuple[str, ...] | None = None) -> None:
        self.context = context
        self.handlers = handlers
        self.queues = queues or (
            "default", "shopify", "alibaba", "webhooks", "orders", "catalog", "media",
            "inventory", "pricing", "procurement", "payments", "fulfillment", "returns",
            "customer_service", "finance", "accounting", "compliance", "maintenance",
        )
        self.worker_id = str(uuid4())
        self.stop_event = asyncio.Event()
        self.retry_decider = RetryDecider(max_attempts=8)

    @property
    def container(self):
        return self.context.services.get("container")

    async def _record_failure(self, task, exc: BaseException) -> None:
        container = self.container
        error = f"{type(exc).__name__}: {exc}"[:4000]
        base_delay = 5.0
        if container is not None:
            routed = container.exception_router.classify(
                exc, operation=task.task_type, payload={"task_id": task.id, "queue": task.queue}
            )
            retry = self.retry_decider.decide(retryable=routed.retryable, attempts=task.attempts)
            if retry.retry:
                base_delay = max(0.1, retry.delay_seconds / max(1, 2 ** min(task.attempts + 1, 8)))
            container.exception_queue.push(routed, next_retry_seconds=retry.delay_seconds if retry.retry else None)
            container.automation_state.record("failed", task.task_type, error)
            await container.event_bus.publish("worker.failed", {
                "task_id": task.id,
                "task_type": task.task_type,
                "category": routed.category,
                "retryable": routed.retryable,
                "error": error,
            })
        await asyncio.to_thread(self.context.queue.fail, task, error, base_delay)

    async def run(self) -> None:
        while not self.stop_event.is_set():
            task = await asyncio.to_thread(self.context.queue.claim, self.worker_id, self.queues)
            if task is None:
                try:
                    await asyncio.wait_for(
                        self.stop_event.wait(), timeout=self.context.settings.worker_poll_interval_seconds
                    )
                except asyncio.TimeoutError:
                    continue
                continue
            handler = self.handlers.get(task.task_type)
            if handler is None:
                await self._record_failure(task, RuntimeError(f"Gestionnaire absent: {task.task_type}"))
                continue
            try:
                result = handler(task.payload)
                if asyncio.iscoroutine(result):
                    result = await result
                await asyncio.to_thread(self.context.queue.complete, task.id)
                if self.container is not None:
                    await self.container.event_bus.publish("worker.completed", {
                        "task_id": task.id, "task_type": task.task_type, "queue": task.queue,
                    })
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                logger.exception("Échec de tâche %s", task.task_type)
                await self._record_failure(task, exc)

    def stop(self) -> None:
        self.stop_event.set()
