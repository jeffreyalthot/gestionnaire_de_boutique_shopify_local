from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from app.config_reloader import ConfigReloader
from app.exception_router import ExceptionRouter
from app.health_aggregator import HealthAggregator
from app.query_bus import QueryBus
from app.service_registry import ServiceRegistry
from app.terminal_session_owner import TerminalSessionOwner
from automation.core.autonomy_controller import AutonomyController
from automation.core.dependency_graph import DependencyGraph
from automation.exceptions.exception_queue import ExceptionQueue
from automation.exceptions.retry_decider import RetryDecider


def test_query_bus_supports_sync_and_async_handlers():
    bus = QueryBus()
    bus.register("sync", lambda payload: payload["value"] + 1)

    async def async_handler(payload):
        return payload["value"] * 2

    bus.register("async", async_handler)
    assert asyncio.run(bus.ask("sync", {"value": 2})) == 3
    assert asyncio.run(bus.ask("async", {"value": 3})) == 6
    assert bus.snapshot()["calls"] == {"sync": 1, "async": 1}


def test_service_registry_rejects_duplicates():
    registry = ServiceRegistry()
    registry.register("db", object(), critical=True, tags=("sqlite", "storage"))
    assert registry.snapshot()["db"]["critical"]
    with pytest.raises(ValueError):
        registry.register("db", object())


def test_health_aggregator_distinguishes_critical_and_warning():
    health = HealthAggregator()
    health.register("critical", lambda: {"ok": True}, critical=True)
    health.register("warning", lambda: {"ok": False})
    report = asyncio.run(health.collect())
    assert report["ok"]
    assert report["status"] == "degraded"
    assert report["warnings"] == ("warning",)


def test_config_reloader_blocks_traversal(tmp_path: Path):
    (tmp_path / "profile.yaml").write_text("workers: 2\ndry_run: true\n", encoding="utf-8")
    loader = ConfigReloader(tmp_path)
    revision = loader.load(("profile.yaml",))
    assert revision.revision
    assert revision.values["profile.yaml"]["workers"] == 2
    with pytest.raises(ValueError):
        loader.load(("../outside.yaml",))


def test_dependency_graph_orders_dependencies_and_detects_cycle():
    graph = DependencyGraph()
    graph.add("publish", ("validate", "media"))
    graph.add("media", ("download",))
    graph.add("validate")
    graph.add("download")
    order = graph.order(("publish",))
    assert order.index("download") < order.index("media") < order.index("publish")
    graph.add("download", ("publish",))
    with pytest.raises(ValueError):
        graph.order()


def test_autonomy_controller_requires_approval_for_financial_live_action():
    controller = AutonomyController(dry_run=False, minimum_confidence=0.9, financial_limit_cad=100)
    assert controller.decide(risk="financial", amount_cad=50).approval_required
    assert controller.decide(risk="financial", amount_cad=50, approved=True).allowed
    assert not controller.decide(risk="financial", amount_cad=101, approved=True).allowed


def test_exception_queue_persists_routed_exception(db):
    routed = ExceptionRouter().classify(TimeoutError("upstream timeout"), operation="catalog")
    queue = ExceptionQueue(db)
    queue.push(routed, next_retry_seconds=0)
    rows = queue.claim_ready()
    assert rows[0]["category"] == "transient"
    assert rows[0]["retryable"] == 1
    queue.resolve(routed.id)
    assert queue.stats()["resolved"] == 1


def test_retry_decider_honours_attempt_limit():
    decider = RetryDecider(max_attempts=2)
    assert decider.decide(retryable=True, attempts=0).retry
    assert not decider.decide(retryable=True, attempts=2).retry
    assert not decider.decide(retryable=False, attempts=0).retry


def test_terminal_session_owner_tracks_single_owner():
    owner = TerminalSessionOwner()
    owner.acquire()
    assert owner.owned
    owner.release()
    assert not owner.owned
