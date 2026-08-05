"""Basic async pytest tests for the AliExpress gateway/client using a mock transport.

These tests are intentionally small and only validate the request/response
flow without hitting the network.
"""

import asyncio
import json

import pytest
import httpx

from config.settings import get_settings
from integrations.aliexpress.gateway import AliExpressGateway
from integrations.aliexpress.client import AliExpressClient


@pytest.mark.asyncio
async def test_search_products_calls_gateway(monkeypatch):
    settings = get_settings()
    # Create a mock HTTPX AsyncClient using MockTransport
    async def handler(request: httpx.Request) -> httpx.Response:
        data = {"products": [{"productId": "123", "name": "mock product"}], "meta": {"page": 1}}
        return httpx.Response(200, json=data)

    transport = httpx.MockTransport(handler)
    async_client = httpx.AsyncClient(transport=transport)
    gateway = AliExpressGateway(settings, client=async_client)
    client = AliExpressClient(gateway)
    res = await client.search_products("test", page=1, page_size=5)
    assert isinstance(res, dict)
    assert "products" in res
