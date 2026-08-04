from __future__ import annotations

from typing import Any

from integrations.shopify.client import ShopifyClient
from workflows.order_intake_workflow import OrderIntakeWorkflow


class ShopifyReconciliationWorkflow:
    def __init__(self, client: ShopifyClient, intake: OrderIntakeWorkflow, *, maximum_pages: int = 20) -> None:
        self.client = client
        self.intake = intake
        self.maximum_pages = max(1, min(int(maximum_pages), 100))

    async def execute(self, query_filter: str = "updated_at:>-24h") -> dict[str, int | str | bool]:
        cursor: str | None = None
        count = pages = duplicates = 0
        seen: set[str] = set()
        for _ in range(self.maximum_pages):
            page = await self.client.orders(first=50, after=cursor, query_filter=query_filter)
            pages += 1
            for edge in page.get("edges", []):
                node = dict(edge.get("node", {}))
                identifier = str(node.get("id", ""))
                if identifier and identifier in seen:
                    duplicates += 1
                    continue
                if identifier:
                    seen.add(identifier)
                await self.intake.execute(node)
                count += 1
            info = page.get("pageInfo", {})
            if not info.get("hasNextPage"):
                return {"orders_reconciled": count, "pages": pages, "duplicates": duplicates, "truncated": False}
            next_cursor = info.get("endCursor")
            if not next_cursor or next_cursor == cursor:
                return {"orders_reconciled": count, "pages": pages, "duplicates": duplicates, "truncated": True, "reason": "pagination_stalled"}
            cursor = str(next_cursor)
        return {"orders_reconciled": count, "pages": pages, "duplicates": duplicates, "truncated": True, "reason": "maximum_pages"}
