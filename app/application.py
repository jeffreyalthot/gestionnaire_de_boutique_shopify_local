from __future__ import annotations

import asyncio

import uvicorn

from api.server import create_app
from app.dependency_container import Container, build_container
from app.graceful_shutdown import cancel_tasks
from app.lifecycle import install_signal_handlers
from automation.execution.operation_handlers import OperationHandlers
from config.paths import NATIVE_PLAN_DIR
from config.settings import Settings
from dashboard.live_dashboard import LiveDashboard
from finance.daily_close import daily_close
from infrastructure.database.backup import backup_database
from infrastructure.native_plan_bridge import NativePlanBridge
from infrastructure.scheduler.job_registry import JobRegistry, ScheduledJob
from infrastructure.scheduler.scheduler import AsyncScheduler
from observability.logger import get_logger
from workers.supervisor import WorkerSupervisor
from workers.worker_context import WorkerContext
from workflows.order_intake_workflow import OrderIntakeWorkflow

logger = get_logger(__name__)


class Application:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.container = build_container(settings)
        self.tasks: list[asyncio.Task] = []
        self.stop_event = asyncio.Event()
        self.dashboard = LiveDashboard(self.container, settings.dashboard_refresh_seconds)
        self.native_plan_bridge = NativePlanBridge(self.container.db, NATIVE_PLAN_DIR)
        self.operation_handlers = OperationHandlers(self.container)
        self.webhook_handlers = self.container.webhook_handlers
        self.scheduler = self._build_scheduler()
        self.worker = self._build_worker()

    def _build_worker(self) -> WorkerSupervisor:
        intake = OrderIntakeWorkflow(
            self.container.db, self.container.pii_vault, self.container.accounting
        )

        async def shopify_webhook(payload: dict[str, object]) -> None:
            topic = str(payload["topic"])
            body = payload["payload"]
            handler_result = self.webhook_handlers.handle(topic, body)
            if topic in {"orders/create", "orders/updated", "orders/paid"}:
                await intake.execute(body)
            for operation in handler_result.get("follow_up_operations", ()):
                self.container.queue.enqueue(
                    "automation_operation",
                    {"operation": operation, "cycle_id": f"webhook:{payload['webhook_id']}", "dry_run": self.settings.app_dry_run},
                    f"webhook-operation:{payload['webhook_id']}:{operation}",
                    queue="automation", priority=25,
                )
            self.container.db.insert_audit("shopify.webhook.handled", "shopify-worker", handler_result)
            self.container.db.mark_event(str(payload["webhook_id"]), "processed")

        async def process_batch(payload: dict[str, object]) -> None:
            await self.container.procurement.submit_batch(str(payload["batch_id"]))

        handlers = {
            "shopify_webhook": shopify_webhook,
            "submit_batch": process_batch,
            "automation_operation": self.operation_handlers.execute,
        }
        context = WorkerContext(
            self.settings, self.container.db, self.container.queue, {"container": self.container}
        )
        return WorkerSupervisor(context, handlers)

    def _build_scheduler(self) -> AsyncScheduler:
        registry = JobRegistry()

        async def automation_tick() -> None:
            if self.settings.automation_enabled:
                await self.container.automation.run_cycle()

        async def batch_tick() -> None:
            batch = self.container.procurement.accumulate_paid_orders()
            decision = self.container.procurement.evaluate_batch(batch)
            if decision["ready"]:
                key = f"submit-batch:{batch['id']}"
                self.container.queue.enqueue(
                    "submit_batch", {"batch_id": batch["id"]}, key,
                    queue="procurement", priority=30,
                )

        async def backup_tick() -> None:
            await asyncio.to_thread(backup_database, self.container.db)

        async def close_tick() -> None:
            await asyncio.to_thread(daily_close, self.container.db)

        async def shopify_reconcile() -> None:
            if self.settings.app_dry_run or not self.settings.live_shopify_ready:
                return
            intake = OrderIntakeWorkflow(
                self.container.db, self.container.pii_vault, self.container.accounting
            )
            page = await self.container.shopify.orders(first=50, query_filter="updated_at:>-24h")
            for edge in page.get("edges", []):
                await intake.execute(edge["node"])

        async def ingest_native_plans() -> None:
            await asyncio.to_thread(self.native_plan_bridge.ingest_pending, 64)

        registry.register(ScheduledJob("automation", self.settings.runtime_cycle_interval_seconds, automation_tick))
        registry.register(ScheduledJob("batching", 30, batch_tick))
        registry.register(ScheduledJob("backup", self.settings.database_backup_interval_seconds, backup_tick, False))
        registry.register(ScheduledJob("daily_close", 3600, close_tick, False))
        registry.register(ScheduledJob("shopify_reconciliation", self.settings.shopify_reconciliation_interval_seconds, shopify_reconcile))
        registry.register(ScheduledJob("native_plan_ingest", 2, ingest_native_plans))
        return AsyncScheduler(registry)

    async def run_once(self) -> dict[str, object]:
        native_plans = await asyncio.to_thread(self.native_plan_bridge.ingest_pending, 64)
        cycle = await self.container.automation.run_cycle() if self.settings.automation_enabled else None
        processed = []
        queues = self.worker.queues
        for _ in range(256):
            task = await asyncio.to_thread(self.container.queue.claim, "run-once", queues, 30)
            if task is None:
                break
            try:
                handler = self.worker.handlers.get(task.task_type)
                if handler is None:
                    raise RuntimeError(f"Gestionnaire absent: {task.task_type}")
                result = handler(task.payload)
                if asyncio.iscoroutine(result):
                    result = await result
                await asyncio.to_thread(self.container.queue.complete, task.id)
                processed.append({"task_id": task.id, "type": task.task_type, "status": "completed", "result": result})
            except Exception as exc:
                await asyncio.to_thread(self.container.queue.fail, task, str(exc))
                self.container.automation_state.record("failed", task.task_type, str(exc))
                processed.append({"task_id": task.id, "type": task.task_type, "status": "failed", "error": str(exc)})
        batch = self.container.procurement.accumulate_paid_orders()
        decision = self.container.procurement.evaluate_batch(batch)
        return {
            "status": self.container.status(),
            "automation_cycle": cycle,
            "processed_tasks": processed,
            "native_plans": native_plans,
            "batch": batch,
            "decision": decision,
        }

    async def run(self, with_dashboard: bool = True, with_api: bool = True) -> None:
        install_signal_handlers(self.stop)
        self.tasks = [
            asyncio.create_task(self.worker.run(), name="worker"),
            asyncio.create_task(self.scheduler.run(), name="scheduler"),
        ]
        if with_dashboard:
            self.tasks.append(asyncio.create_task(self.dashboard.run(), name="dashboard"))
        if with_api:
            config = uvicorn.Config(
                create_app(self.container), host=self.settings.app_host, port=self.settings.app_port,
                log_level=self.settings.app_log_level.lower(), loop="asyncio",
            )
            server = uvicorn.Server(config)
            self.tasks.append(asyncio.create_task(server.serve(), name="api"))
        try:
            await self.stop_event.wait()
        finally:
            self.worker.stop()
            self.scheduler.stop()
            self.dashboard.stop()
            await cancel_tasks(self.tasks)
            await self.container.close()

    def stop(self) -> None:
        if not self.stop_event.is_set():
            self.stop_event.set()
