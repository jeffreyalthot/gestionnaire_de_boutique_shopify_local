from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field
class WebhookReceipt(BaseModel):
    model_config = ConfigDict(extra="forbid")
    accepted: bool
    duplicate: bool = False
    webhook_id: str = Field(default="", max_length=255)
    queued_task_id: str = Field(default="", max_length=255)
