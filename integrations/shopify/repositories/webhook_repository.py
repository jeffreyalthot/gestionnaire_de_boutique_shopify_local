from __future__ import annotations

from typing import Any

from integrations.shopify.repositories.base_repository import ShopifyRepository


class WebhookRepository(ShopifyRepository):
    resource = "webhooks"

    async def list(self) -> list[dict[str, Any]]:
        return list(await self._call("list", self.client.webhooks))

    async def create(self, topic: str, uri: str) -> dict[str, Any]:
        if not topic or not uri:
            raise ValueError("topic and uri are required")
        return await self._call("create", self.client.create_webhook, topic, uri)

    async def missing(self, desired: dict[str, str]) -> dict[str, str]:
        existing = await self.list()
        pairs = {(str(item.get("topic", "")), str(item.get("uri", ""))) for item in existing}
        return {topic: uri for topic, uri in desired.items() if (topic, uri) not in pairs}
