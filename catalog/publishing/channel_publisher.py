from __future__ import annotations

from typing import Any


class ChannelPublisher:
    MUTATION = """mutation publishablePublish($id: ID!, $input: [PublicationInput!]!) { publishablePublish(id: $id, input: $input) { publishable { availablePublicationsCount { count } } userErrors { field message } } }"""

    def __init__(self, transport: Any) -> None:
        self.transport = transport

    async def publish(self, product_id: str, publication_ids: tuple[str, ...], *, dry_run: bool = True) -> dict[str, object]:
        inputs = [{"publicationId": identifier} for identifier in sorted(set(publication_ids))]
        if dry_run:
            return {"status": "simulated", "product_id": product_id, "publications": inputs}
        data = await self.transport.execute(self.MUTATION, {"id": product_id, "input": inputs})
        payload = data.get("publishablePublish", data)
        errors = payload.get("userErrors", [])
        return {"status": "failed" if errors else "published", "errors": errors, "payload": payload}
