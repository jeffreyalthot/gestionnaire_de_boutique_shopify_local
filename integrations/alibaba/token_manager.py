from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256

from config.settings import Settings


@dataclass(frozen=True, slots=True)
class AlibabaTokenStatus:
    access_configured: bool
    refresh_configured: bool
    access_fingerprint: str
    app_key_configured: bool

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class AlibabaTokenManager:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def access_token(self) -> str:
        token = self.settings.alibaba_access_token.get_secret_value()
        if not token:
            raise RuntimeError("Alibaba access token is not configured")
        return token

    def refresh_token(self) -> str:
        token = self.settings.alibaba_refresh_token.get_secret_value()
        if not token:
            raise RuntimeError("Alibaba refresh token is not configured")
        return token

    def status(self) -> AlibabaTokenStatus:
        access = self.settings.alibaba_access_token.get_secret_value()
        refresh = self.settings.alibaba_refresh_token.get_secret_value()
        return AlibabaTokenStatus(
            bool(access), bool(refresh), sha256(access.encode("utf-8")).hexdigest()[:12] if access else "",
            bool(self.settings.alibaba_app_key),
        )
