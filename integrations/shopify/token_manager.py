from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256

from config.settings import Settings


@dataclass(frozen=True, slots=True)
class TokenStatus:
    configured: bool
    fingerprint: str
    shop_domain: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class ShopifyTokenManager:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def access_token(self) -> str:
        token = self.settings.shopify_admin_access_token.get_secret_value()
        if not token:
            raise RuntimeError("Shopify access token is not configured")
        return token

    def configured(self) -> bool:
        return self.settings.live_shopify_ready

    def status(self) -> TokenStatus:
        token = self.settings.shopify_admin_access_token.get_secret_value()
        fingerprint = sha256(token.encode("utf-8")).hexdigest()[:12] if token else ""
        return TokenStatus(bool(self.settings.live_shopify_ready), fingerprint, str(self.settings.shopify_shop_domain))
