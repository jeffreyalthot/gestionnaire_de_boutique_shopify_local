from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field
class DashboardResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    counts: dict[str, int] = Field(default_factory=dict)
    finance: dict[str, float] = Field(default_factory=dict)
    runtime: dict[str, object] = Field(default_factory=dict)
    queues: dict[str, int] = Field(default_factory=dict)
    alerts: list[str] = Field(default_factory=list, max_length=100)
