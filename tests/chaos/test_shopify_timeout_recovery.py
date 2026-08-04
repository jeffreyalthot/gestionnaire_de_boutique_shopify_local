from infrastructure.http.adaptive_timeout import AdaptiveTimeout

def test_shopify_timeout_recovers_after_fast_samples():
    timeout=AdaptiveTimeout(minimum=3,maximum=30,window=4,multiplier=2)
    timeout.observe(20); assert timeout.value()==30
    for _ in range(4): timeout.observe(2)
    assert timeout.value()==4
