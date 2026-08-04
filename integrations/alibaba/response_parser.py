from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class AlibabaResponse:
    node: dict[str, object]
    request_id: str
    success: bool
    error_code: str
    error_message: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def first_response_node(payload: dict[str, object]) -> dict[str, object]:
    for key, value in payload.items():
        if key.endswith("_response") and isinstance(value, dict):
            return value
    return payload


def parse_response(payload: dict[str, object]) -> AlibabaResponse:
    if not isinstance(payload, dict):
        raise TypeError("Alibaba response must be an object")
    node = first_response_node(payload)
    error = node.get("error_response", node.get("error", {})) if isinstance(node, dict) else {}
    if not isinstance(error, dict):
        error = {"message": str(error)}
    code = str(error.get("code", node.get("code", "")))
    message = str(error.get("msg", error.get("message", node.get("message", ""))))
    success = not bool(code or message.lower().startswith("error"))
    request_id = str(node.get("request_id", node.get("requestId", payload.get("request_id", ""))))
    return AlibabaResponse(dict(node), request_id, success, code, message)
