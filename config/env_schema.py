from pydantic import BaseModel, Field

class CredentialStatus(BaseModel):
    name: str
    configured: bool
    required_for_live: bool
    detail: str = Field(default="")
