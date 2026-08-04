from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OrderException:
    code: str
    message: str
    retryable: bool = False
    hold_required: bool = True
