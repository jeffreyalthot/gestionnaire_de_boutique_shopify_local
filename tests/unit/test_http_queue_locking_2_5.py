from __future__ import annotations

import asyncio
from pathlib import Path

import httpx
import pytest

from infrastructure.http.async_client import ManagedAsyncClient, create_async_client
from infrastructure.http.backoff import BackoffPolicy
from infrastructure.http.retry import RetryPolicy, execute_with_retry, retry_async
from infrastructure.locking.process_lock import ProcessLock
from infrastructure.locking.resource_lock import ResourceLockRegistry
from infrastructure.queue.task import QueueTask
from infrastructure.queue.task_claim import claim
from infrastructure.queue.task_serializer import TaskSerializationError, deserialize_task, serialize_task, task_fingerprint
from integrations.alibaba.retry_policy import decide_retry as alibaba_retry
from integrations.shopify.retry_policy import decide_retry as shopify_retry


def test_async_client_configuration_is_bounded():
    client = create_async_client(5, max_connections=2, max_keepalive_connections=1)
    assert client.headers["User-Agent"].endswith("/2.5")
    asyncio.run(client.aclose())


def test_managed_client_records_mock_transport():
    async def scenario():
        transport = httpx.MockTransport(lambda request: httpx.Response(200, content=b"ok"))
        managed = ManagedAsyncClient(httpx.AsyncClient(transport=transport))
        response = await managed.get("https://example.test")
        assert response.text == "ok"
        assert managed.metrics.snapshot()["requests"] == 1
        await managed.aclose()
    asyncio.run(scenario())


def test_retry_policy_retries_selected_exceptions_without_sleep():
    async def scenario():
        count = 0
        async def action():
            nonlocal count
            count += 1
            if count < 3:
                raise TimeoutError("temporary")
            return "ok"
        policy = RetryPolicy(attempts=3, backoff=BackoffPolicy(0, 0, 0, 1))
        result = await execute_with_retry(action, policy)
        assert result.value == "ok" and result.attempts == 3 and len(result.history) == 2
    asyncio.run(scenario())


def test_retry_async_preserves_historical_attempt_semantics():
    async def scenario():
        count = 0
        async def action():
            nonlocal count
            count += 1
            if count == 1:
                raise ValueError("once")
            return count
        assert await retry_async(action, 1, retryable_exceptions=(ValueError,)) == 2
    asyncio.run(scenario())


def test_resource_lock_serializes_and_prunes():
    async def scenario():
        registry = ResourceLockRegistry(maximum_locks=16)
        order = []
        async def worker(number):
            async with registry.hold("sku:1"):
                order.append(number)
                await asyncio.sleep(0)
        await asyncio.gather(worker(1), worker(2))
        assert sorted(order) == [1, 2]
        assert registry.statistics()["acquisitions"] == 2
        assert registry.prune() == 1
    asyncio.run(scenario())


def test_process_lock_uses_recoverable_file_lock(tmp_path: Path):
    first = ProcessLock(tmp_path / "app.lock")
    second = ProcessLock(tmp_path / "app.lock")
    first.acquire()
    with pytest.raises(RuntimeError):
        second.acquire()
    first.release()
    second.acquire(); second.release()


def test_queue_task_round_trip_and_fingerprint():
    task = QueueTask("1", "orders", "process", {"id": 1}, 5, 0, 3, "key")
    encoded = serialize_task(task)
    decoded = deserialize_task(encoded)
    assert decoded.id == "1" and decoded.retryable
    assert task_fingerprint(task) == task_fingerprint(decoded)


def test_queue_task_serializer_rejects_invalid_and_oversize():
    with pytest.raises(TaskSerializationError):
        deserialize_task("[]")
    task = QueueTask("1", "q", "t", {"value": "x" * 100}, 0, 0, 1, "k")
    with pytest.raises(TaskSerializationError, match="too_large"):
        serialize_task(task, maximum_bytes=20)


def test_claim_validates_worker_and_queue_names():
    class Queue:
        def claim(self, worker, names):
            return None
    with pytest.raises(ValueError):
        claim(Queue(), "", ("q",))
    result = claim(Queue(), "w", ("q", "q"))
    assert result.queues == ("q",) and not result.claimed


def test_platform_retry_policies_use_status_and_retry_after():
    shopify = shopify_retry(1, status_code=429, headers={"Retry-After": "7"})
    assert shopify.retry and shopify.delay_seconds == 7
    assert not shopify_retry(1, status_code=400).retry
    alibaba = alibaba_retry(1, error_code="isv.SYSTEM_BUSY", headers={"retry-after": "3"})
    assert alibaba.retry and alibaba.delay_seconds == 3
