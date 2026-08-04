from infrastructure.http.adaptive_timeout import AdaptiveTimeout

def test_alibaba_timeout_is_adaptive_and_bounded():
    timeout=AdaptiveTimeout(minimum=2,maximum=15,multiplier=2)
    for value in (1,2,9,40): timeout.observe(value)
    assert 2 <= timeout.value() <= 15
