from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
class HealthResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: Literal["ok", "degraded", "failed"]
    database: dict[str, object] = Field(default_factory=dict)
    ai: dict[str, object] = Field(default_factory=dict)
    shopify: dict[str, object] = Field(default_factory=dict)
    alibaba: dict[str, object] = Field(default_factory=dict)
    uptime_seconds: float = Field(default=0, ge=0)
