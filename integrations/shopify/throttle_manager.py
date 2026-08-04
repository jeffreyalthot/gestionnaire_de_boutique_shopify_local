from __future__ import annotations
import asyncio
from integrations.shopify.graphql_cost_budget import CostSnapshot, GraphqlCostBudget

class ShopifyThrottleManager:
    def __init__(self, minimum_available: int = 100) -> None:
        self.budget = GraphqlCostBudget(minimum_available=minimum_available)

    @property
    def last_available(self) -> float:
        return self.budget.snapshot().currently_available

    async def before_request(self, estimated_cost: int = 10, *, maximum_wait_seconds: float = 30.0) -> float:
        wait = min(maximum_wait_seconds, self.budget.seconds_until_available(estimated_cost))
        if wait > 0:
            await asyncio.sleep(wait)
        self.budget.reserve(estimated_cost)
        return wait

    async def observe(self, extensions: dict[str, object] | None) -> CostSnapshot:
        return self.budget.observe(extensions)
