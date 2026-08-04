from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from ai.features.feature_store import FeatureStore
from ai.runtime.model_unloader import unload_all, unload_model
from app.graceful_shutdown import cancel_tasks
from app.lifecycle import ApplicationLifecycle
from app.liveness import heartbeat, liveness
from dashboard.formatter import bytes_size, duration, money, percentage, truncate
from dashboard.theme import status_marker, status_theme
from infrastructure.cache.cache_keys import cache_key
from infrastructure.database.engine import Database


def test_feature_store_version_merge_and_conflict(tmp_path: Path):
    db = Database(tmp_path / "features.sqlite3"); db.initialize()
    store = FeatureStore(db, max_features=4)
    first = store.put("product", "p1", {"margin": 0.2})
    assert first.version == 1 and store.get("product", "p1") == {"margin": 0.2}
    second = store.put("product", "p1", {"demand": 0.9}, merge=True, expected_version=1)
    assert second.version == 2 and second.features == {"demand": 0.9, "margin": 0.2}
    with pytest.raises(RuntimeError, match="version_conflict"):
        store.put("product", "p1", {"margin": 0.3}, expected_version=1)
    assert store.delete("product", "p1") is True
    assert store.get("product", "p1") == {}


def test_feature_store_rejects_invalid_features(tmp_path: Path):
    db = Database(tmp_path / "features.sqlite3"); db.initialize()
    store = FeatureStore(db, max_features=1)
    with pytest.raises(ValueError, match="feature_limit"):
        store.put("product", "p1", {"a": 1, "b": 2})
    with pytest.raises(ValueError, match="non_finite"):
        store.put("product", "p1", {"a": float("inf")})


def test_model_unloader_calls_cleanup_and_reports():
    class Model:
        closed = False
        def close(self):
            self.closed = True

    model = Model()
    registry = {"m": model}
    result = unload_model(registry, "m", collect=False)
    assert result.removed and result.cleanup_called and model.closed and not registry
    registry.update({"a": object(), "b": object()})
    assert len(unload_all(registry)) == 2 and not registry


def test_cache_keys_are_canonical_and_bounded():
    assert cache_key("Product", {"b": 2, "a": 1}) == 'product:{"a":1,"b":2}'
    long_key = cache_key("product", "x" * 500, max_length=80)
    assert len(long_key) == 80 and long_key.startswith("product:")
    with pytest.raises(ValueError):
        cache_key("bad:name", 1)


def test_lifecycle_enforces_transitions_and_stop():
    lifecycle = ApplicationLifecycle()
    lifecycle.transition("starting")
    lifecycle.transition("running")
    stopped = lifecycle.request_stop("operator")
    assert stopped.state == "stopping" and stopped.stop_requested and stopped.reason == "operator"
    lifecycle.transition("stopped")
    with pytest.raises(RuntimeError):
        ApplicationLifecycle().transition("running")


def test_liveness_heartbeat_sequence():
    before = liveness()
    after = heartbeat()
    assert after["ok"] is True and after["heartbeat_sequence"] == before["heartbeat_sequence"] + 1


def test_dashboard_formatters_and_theme():
    assert duration(90061) == "01j 01h 01m 01s"
    assert money("1234.555") == "1 234.56 CAD"
    assert percentage(0.125) == "12.5 %"
    assert bytes_size(1024) == "1.0 Kio"
    assert truncate("abcdef", 5) == "ab..."
    assert status_theme("error").style == "bold red"
    assert status_marker("running").startswith("[>")


def test_graceful_shutdown_cancels_tasks():
    async def scenario():
        async def sleeper():
            await asyncio.sleep(10)
        tasks = [asyncio.create_task(sleeper()), asyncio.create_task(sleeper())]
        result = await cancel_tasks(tasks, timeout=1)
        assert result.requested == 2 and result.cancelled == 2 and result.timed_out == 0
    asyncio.run(scenario())
