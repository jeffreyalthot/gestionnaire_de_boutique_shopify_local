from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class AlibabaRequest:
    method: str
    parameters: dict[str, object]
    session_required: bool

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def encode_business_parameters(data: Mapping[str, object]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in data.items():
        name = str(key).strip()
        if not name or value is None:
            continue
        if isinstance(value, (dict, list, tuple)):
            result[name] = json.dumps(value, separators=(",", ":"), ensure_ascii=False, default=str)
        elif isinstance(value, bool):
            result[name] = "true" if value else "false"
        else:
            result[name] = value
    return result


def build_request(method: str, parameters: Mapping[str, object] | None = None, *,
                  session_required: bool = True) -> AlibabaRequest:
    method_name = str(method).strip()
    if not method_name or "." not in method_name:
        raise ValueError("Alibaba method name is invalid")
    return AlibabaRequest(method_name, encode_business_parameters(parameters or {}), bool(session_required))
