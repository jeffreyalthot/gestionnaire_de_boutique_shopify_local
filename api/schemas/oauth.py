from __future__ import annotations
from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field
class OAuthStartResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    url: AnyHttpUrl
    state: str = Field(min_length=16, max_length=512)
    expires_in_seconds: int = Field(default=600, ge=30, le=3600)
