from __future__ import annotations

import hashlib
import hmac
import re


class CustomerIdentityResolver:
    EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def __init__(self, salt: str) -> None:
        if not salt:
            raise ValueError("Un sel d'identité est requis.")
        self._salt = salt.encode("utf-8")

    def email_hash(self, email: str) -> str:
        normalized = email.strip().casefold()
        if not self.EMAIL.fullmatch(normalized):
            raise ValueError("Adresse courriel invalide.")
        return hmac.new(self._salt, normalized.encode("utf-8"), hashlib.sha256).hexdigest()

    def match(self, left_hash: str, right_hash: str) -> bool:
        return bool(left_hash and right_hash and hmac.compare_digest(left_hash, right_hash))
