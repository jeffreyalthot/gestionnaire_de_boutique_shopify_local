import pytest

from workers.analytics_worker import AnalyticsWorker
from workers.worker_budget import WorkerBudget
from workers.worker_registry import WorkerDescriptor, WorkerRegistry


@pytest.mark.asyncio
async def test_specialized_worker_routes_and_rejects():
    worker = AnalyticsWorker(lambda payload: {'value': payload['value'] + 1})
    completed = await worker.run_once('analytics_snapshot', {'value': 2})
    rejected = await worker.run_once('payment_status', {})
    assert completed.result == {'value': 3}
    assert rejected.status == 'rejected'


def test_worker_budget_is_limited_to_dual_core():
    with pytest.raises(ValueError):
        WorkerBudget(3)


def test_worker_registry_rejects_duplicate_task_route():
    registry = WorkerRegistry()
    registry.register(WorkerDescriptor('a', 'q', ('task',)), object())
    registry.register(WorkerDescriptor('b', 'q', ('task',)), object())
    with pytest.raises(ValueError):
        registry.task_routes()
