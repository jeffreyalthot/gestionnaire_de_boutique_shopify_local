from __future__ import annotations
import base64
import binascii
import hashlib
import hmac

def shopify_hmac(body: bytes, secret: str) -> str:
    if not secret:
        raise ValueError("Le secret Shopify est requis")
    return base64.b64encode(hmac.new(secret.encode("utf-8"), body, hashlib.sha256).digest()).decode("ascii")

def verify_shopify_hmac(body: bytes, received: str, secret: str, *, max_body_bytes: int | None = None) -> bool:
    if not secret or not received or not isinstance(body, (bytes, bytearray)):
        return False
    if max_body_bytes is not None and len(body) > max_body_bytes:
        return False
    try:
        supplied = base64.b64decode(received.strip(), validate=True)
    except (binascii.Error, ValueError):
        return False
    expected = hmac.new(secret.encode("utf-8"), bytes(body), hashlib.sha256).digest()
    return len(supplied) == len(expected) and hmac.compare_digest(expected, supplied)
