import hashlib

def build_idempotency_key(namespace: str, *parts: object) -> str:
    raw = "|".join([namespace, *(str(part) for part in parts)])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
