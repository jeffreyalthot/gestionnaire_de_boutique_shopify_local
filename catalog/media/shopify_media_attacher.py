from __future__ import annotations

from typing import Any


class ShopifyMediaAttacher:
    MUTATION = """mutation productCreateMedia($productId: ID!, $media: [CreateMediaInput!]!) { productCreateMedia(productId: $productId, media: $media) { media { id status } mediaUserErrors { field message code } } }"""

    def __init__(self, transport: Any) -> None:
        self.transport = transport

    async def attach(self, product_id: str, resource_urls: list[str], alt_texts: list[str]) -> list[dict[str, Any]]:
        media = [{"originalSource": url, "mediaContentType": "IMAGE", "alt": alt_texts[index] if index < len(alt_texts) else ""} for index, url in enumerate(resource_urls)]
        data = await self.transport.execute(self.MUTATION, {"productId": product_id, "media": media})
        payload = data.get("productCreateMedia", data)
        errors = payload.get("mediaUserErrors", [])
        if errors:
            raise ValueError(f"Association média refusée: {errors}")
        return list(payload.get("media", []))
