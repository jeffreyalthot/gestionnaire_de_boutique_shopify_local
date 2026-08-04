from __future__ import annotations

import hashlib
import hmac
import time
from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class SignedRequest:
    timestamp: int
    nonce: str
    signature: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class RequestSigner:
    def __init__(self, secret: str, *, tolerance_seconds: int = 300) -> None:
        if not secret:
            raise ValueError("secret requis")
        self.secret = secret.encode("utf-8")
        self.tolerance = max(1, int(tolerance_seconds))
        self._seen: dict[str, int] = {}

    def sign(self, payload: bytes, *, timestamp: int | None = None, nonce: str = "") -> SignedRequest:
        ts = int(time.time() if timestamp is None else timestamp)
        canonical = self._canonical(payload, ts, nonce)
        return SignedRequest(ts, nonce, hmac.new(self.secret, canonical, hashlib.sha256).hexdigest())

    def verify(self, payload: bytes, signed: SignedRequest, *, now: int | None = None, prevent_replay: bool = True) -> bool:
        current = int(time.time() if now is None else now)
        self._purge(current)
        if abs(current - int(signed.timestamp)) > self.tolerance:
            return False
        replay_key = f"{signed.timestamp}:{signed.nonce}:{signed.signature}"
        if prevent_replay and replay_key in self._seen:
            return False
        expected = self.sign(payload, timestamp=signed.timestamp, nonce=signed.nonce).signature
        valid = hmac.compare_digest(expected, signed.signature)
        if valid and prevent_replay:
            self._seen[replay_key] = current
        return valid

    @staticmethod
    def _canonical(payload: bytes, timestamp: int, nonce: str) -> bytes:
        return str(timestamp).encode() + b"." + nonce.encode() + b"." + bytes(payload)

    def _purge(self, now: int) -> None:
        self._seen = {key: created for key, created in self._seen.items() if now - created <= self.tolerance}


def hmac_sha256_hex(secret: str, payload: bytes) -> str:
    return hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
