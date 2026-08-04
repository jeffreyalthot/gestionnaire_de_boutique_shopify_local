from __future__ import annotations
import base64
import hashlib
import os
from cryptography.fernet import Fernet, InvalidToken

def derive_fernet_key(secret: str) -> bytes:
    if not secret:
        secret = os.environ.get("COMPUTERNAME") or os.environ.get("HOSTNAME") or "local-orchestrator"
    digest = hashlib.sha256(secret.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest)

class EncryptionService:
    def __init__(self, secret: str) -> None:
        self._fernet = Fernet(derive_fernet_key(secret))
    def encrypt(self, plaintext: str) -> str:
        return self._fernet.encrypt(plaintext.encode("utf-8")).decode("ascii")
    def decrypt(self, ciphertext: str) -> str:
        try:
            return self._fernet.decrypt(ciphertext.encode("ascii")).decode("utf-8")
        except InvalidToken as exc:
            raise ValueError("Donnée chiffrée invalide ou clé incorrecte.") from exc
