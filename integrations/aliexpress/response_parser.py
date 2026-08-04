"""Parse AliExpress responses into a small uniform shape for the gateway.

The parser returns a dict with optional request_id and keeps the original payload
available for callers.
"""
from __future__ import annotations

from typing import Any, Dict


def parse_response(payload: Dict[str, Any]) -> Dict[str, Any]:
    # Many AliExpress endpoints return an object with a request_id under different keys.
    request_id = payload.get("request_id") or payload.get("requestId") or payload.get("trace_id")
    return {"request_id": request_id, "payload": payload}
