from domain.value_objects.idempotency_key import build_idempotency_key
def test_key_stable(): assert build_idempotency_key("x",1)==build_idempotency_key("x",1)
