from __future__ import annotations
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, field_validator
class ShippingRate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    service_name: str = Field(min_length=1, max_length=128)
    service_code: str = Field(min_length=1, max_length=64)
    total_price: Decimal = Field(ge=0)
    currency: str = Field(min_length=3, max_length=3)
    min_delivery_date: str | None = None
    max_delivery_date: str | None = None
    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, value: str) -> str:
        return value.upper()
