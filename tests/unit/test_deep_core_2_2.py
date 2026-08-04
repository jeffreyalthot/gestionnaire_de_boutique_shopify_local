from __future__ import annotations
import time
from pathlib import Path
import pytest
from ai.features.customer_features import customer_features
from ai.features.order_features import order_features
from ai.features.product_features import product_features
from finance.currency_gain_loss import calculate_currency_gain_loss
from finance.gross_profit_calculator import calculate_gross_profit
from finance.net_profit_calculator import calculate_net_profit
from finance.refund_reserve import calculate_refund_reserve
from infrastructure.cache.memory_cache import MemoryCache
from infrastructure.cache.ttl_cache import TTLCache
from infrastructure.http.response_cache import ResponseCache
from infrastructure.locking.file_lock import FileLock
from security.webhook_security import shopify_hmac, verify_shopify_hmac

def test_feature_extractors_are_finite_and_rich():
    assert customer_features({"orders_count": 2, "total_spent": 100})["average_order_value"] == 50
    assert order_features({"total_amount": 60, "lines": [{"quantity": 2}]})["item_quantity"] == 2
    assert product_features({"sale_price_cad": 20, "landed_cost_cad": 10})["markup"] == 1

def test_finance_breakdowns_use_cent_precision():
    gross = calculate_gross_profit("100.005", "40.001", "10")
    assert str(gross.gross_profit) == "50.01"
    net = calculate_net_profit(100, 10, 20, 5)
    assert net.net_profit == 65
    reserve = calculate_refund_reserve(100, 2.5)
    assert reserve.reserve == pytest.approx(2.5)
    assert calculate_currency_gain_loss(100, 98).favorable

def test_cache_lru_ttl_and_stats():
    cache = MemoryCache[int](max_entries=2, max_estimated_bytes=1_000_000)
    cache.set("a", 1, 10); cache.set("b", 2, 10)
    assert cache.get("a") == 1
    cache.set("c", 3, 10)
    assert cache.get("b") is None
    assert cache.stats().evictions == 1

def test_ttl_cache_expiration():
    cache = TTLCache[int](default_ttl=0.01)
    cache.put("x", 1); time.sleep(0.02)
    assert cache.get("x") is None
    assert cache.stats().expirations >= 1

def test_response_cache_key_is_stable():
    assert ResponseCache.key("get", "https://x", {"b": 2, "a": 1}) == ResponseCache.key("GET", "https://x", {"a": 1, "b": 2})

def test_file_lock_context_and_stale_recovery(tmp_path: Path):
    path = tmp_path / "runtime.lock"
    with FileLock(path):
        assert path.exists()
        with pytest.raises(RuntimeError): FileLock(path).acquire()
    assert not path.exists()
    path.write_text('{"created_at":0}', encoding="utf-8")
    lock = FileLock(path, stale_after_seconds=1); lock.acquire(); lock.release()

def test_shopify_hmac_strict_base64_and_body_limit():
    body = b'{"id":1}'; signature = shopify_hmac(body, "secret")
    assert verify_shopify_hmac(body, signature, "secret", max_body_bytes=100)
    assert not verify_shopify_hmac(body, "not-base64!", "secret")
    assert not verify_shopify_hmac(body, signature, "secret", max_body_bytes=1)
