from __future__ import annotations

from typing import Any

from fulfillment.fulfillment_plan import FulfillmentPlan


class FulfillmentRepository:
    def __init__(self, db: Any) -> None: self.db=db

    def save(self, plan: FulfillmentPlan) -> None:
        self.db.set_value(f"fulfillment-plan:{plan.order_id}", plan.as_dict())

    def get(self, order_id: str) -> dict[str, Any] | None:
        return self.db.get_value(f"fulfillment-plan:{order_id}")
