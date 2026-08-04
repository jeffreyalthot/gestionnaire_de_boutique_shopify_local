import asyncio
from automation.exceptions.exception_classifier import ExceptionClassifier
from infrastructure.http.circuit_breaker import CircuitBreaker
from infrastructure.queue.durable_queue import DurableQueue
from infrastructure.queue.dead_letter_queue import DeadLetterQueue
from security.idempotency import IdempotencyRegistry
from observability.health_registry import HealthRegistry

def test_exception_classifier_redacts_and_routes():
    row=ExceptionClassifier().classify(PermissionError("bad HMAC signature"),payload={"token":"secret"});assert row.category=="security" and row.payload["token"]=="***"
def test_idempotency_registry():
    registry=IdempotencyRegistry();assert registry.reserve("k");assert not registry.reserve("k");registry.complete("k",{"ok":1});assert registry.get("k")=={"ok":1}
def test_circuit_breaker_states():
    breaker=CircuitBreaker(failures=2,reset_seconds=60);assert breaker.allow();breaker.failure();breaker.failure();assert not breaker.allow() and breaker.snapshot().state=="open";breaker.success();assert breaker.allow()
def test_durable_queue_batch_heartbeat_cancel(db):
    queue=DurableQueue(db);ids=queue.enqueue_many([{"task_type":"a","payload":{"n":1},"idempotency_key":"1"},{"task_type":"b","payload":{"n":2},"idempotency_key":"2"}]);assert len(ids)==2
    tasks=queue.claim_many("w",limit=2);assert len(tasks)==2 and queue.heartbeat(tasks[0].id,"w");queue.complete(tasks[0].id);assert queue.cancel(tasks[1].id)
    assert queue.stats()["completed"]==1 and queue.stats()["cancelled"]==1
async def _health():
    registry=HealthRegistry();registry.register("ok",lambda:{"ok":True},critical=True);row=await registry.collect();assert row["ok"] and registry.trend()["healthy"]==1
def test_health_registry():asyncio.run(_health())
