import hashlib, hmac, json


class SessionIntegrity:
    def __init__(self, secret: bytes) -> None:
        if len(secret)<16: raise ValueError("secret trop court")
        self.secret=secret
    def sign(self, payload: dict[str,object]) -> str:
        raw=json.dumps(payload,sort_keys=True,separators=(",",":"),default=str).encode(); return hmac.new(self.secret,raw,hashlib.sha256).hexdigest()
    def verify(self, payload: dict[str,object], signature: str) -> bool: return hmac.compare_digest(self.sign(payload),signature)
