from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field, model_validator

class ApprovalDecision(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    approved: bool
    actor: str = Field(min_length=1, max_length=128)
    reason: str = Field(default="", max_length=1000)

    @model_validator(mode="after")
    def validate_reason(self) -> "ApprovalDecision":
        if not self.approved and not self.reason:
            raise ValueError("Une raison est requise pour un refus.")
        return self
