"""Simple request helpers for AliExpress.

Currently the Open Platform is REST/JSON-based. This module centralizes any
encoding/parameter decisions so the gateway and client can stay simple.
"""
from __future__ import annotations

from typing import Dict, Any


def build_query_params(params: Dict[str, Any] | None) -> Dict[str, Any]:
    # Flatten boolean/None values and ensure simple strings for httpx
    out: Dict[str, Any] = {}
    if not params:
        return out
    for k, v in params.items():
        if v is None:
            continue
        if isinstance(v, bool):
            out[k] = str(v).lower()
        else:
            out[k] = v
    return out
