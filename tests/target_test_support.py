from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from integrations.alibaba.contract_validator import AlibabaContractValidator
from integrations.shopify.graphql_document_loader import GraphQLDocumentLoader

ROOT = Path(__file__).resolve().parents[1]


def assert_alibaba_contract(name: str, payload: dict[str, Any]) -> None:
    assert AlibabaContractValidator().validate(name, payload) == payload


def assert_graphql_document(path: str, operation: str | None = None) -> str:
    text = GraphQLDocumentLoader().load(path)
    assert text.startswith(("query ", "mutation ", "subscription "))
    if operation:
        assert operation in text
    assert "{" in text and "}" in text
    return text


def assert_json_file(path: str) -> dict[str, Any]:
    value = json.loads((ROOT / path).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value
