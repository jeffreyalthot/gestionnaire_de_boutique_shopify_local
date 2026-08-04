from __future__ import annotations

from typing import Any


class PublishCompensator:
    MUTATION = """mutation publishableUnpublish($id: ID!, $input: [PublicationInput!]!) { publishableUnpublish(id: $id, input: $input) { userErrors { field message } } }"""

    def __init__(self, transport: Any) -> None:
        self.transport = transport

    async def unpublish(self, product_id: str, publication_ids: tuple[str, ...], *, dry_run: bool = True) -> dict[str, object]:
        inputs = [{"publicationId": identifier} for identifier in sorted(set(publication_ids))]
        if dry_run:
            return {"status": "simulated", "product_id": product_id, "publications": inputs}
        data = await self.transport.execute(self.MUTATION, {"id": product_id, "input": inputs})
        payload = data.get("publishableUnpublish", data)
        errors = payload.get("userErrors", [])
        return {"status": "failed" if errors else "unpublished", "errors": errors}
