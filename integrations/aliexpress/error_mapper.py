"""Error mapping for AliExpress responses.

Implement a conservative inspector that raises for obvious API errors and
normalizes message shape for the response parser.
"""
from __future__ import annotations

from typing import Any, Dict


class AliExpressAPIError(Exception):
    pass


def inspect_aliexpress_response(payload: Dict[str, Any]) -> None:
    # AliExpress responses often include an "error_response" or "error" key on failure.
    if not isinstance(payload, dict):
        raise AliExpressAPIError("Invalid payload type")
    if "error_response" in payload:
        err = payload["error_response"]
        code = err.get("code")
        message = err.get("msg") or err.get("message") or str(err)
        raise AliExpressAPIError(f"AliExpress API error: {code} {message}")
    # Some endpoints use a top-level success flag
    if payload.get("success") is False:
        message = payload.get("message") or payload.get("msg") or "Unknown error"
        raise AliExpressAPIError(f"AliExpress API error: {message}")
