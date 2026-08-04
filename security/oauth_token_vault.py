from __future__ import annotations

from security.encryption import CipherBox


class OAuthTokenVault:
    def __init__(self, cipher: CipherBox) -> None: self.cipher=cipher; self._tokens: dict[str,str]={}
    def put(self, provider: str, token: str) -> None: self._tokens[provider]=self.cipher.encrypt(token)
    def get(self, provider: str) -> str | None:
        value=self._tokens.get(provider); return self.cipher.decrypt(value) if value else None
    def delete(self, provider: str) -> None: self._tokens.pop(provider,None)
