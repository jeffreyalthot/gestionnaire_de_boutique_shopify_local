from __future__ import annotations
from collections.abc import AsyncIterator, Awaitable, Callable
from typing import Any

async def paginate(fetch_page: Callable[[str | None], Awaitable[dict[str, Any]]], *, max_pages: int = 1000) -> AsyncIterator[dict[str, object]]:
    if max_pages < 1:
        raise ValueError("max_pages doit être positif")
    cursor: str | None = None
    seen: set[str] = set()
    for _ in range(max_pages):
        page = await fetch_page(cursor)
        edges = page.get("edges", [])
        if not isinstance(edges, list):
            raise ValueError("Réponse paginée invalide: edges doit être une liste")
        for edge in edges:
            if isinstance(edge, dict) and isinstance(edge.get("node"), dict):
                yield edge["node"]
        info = page.get("pageInfo", {})
        if not isinstance(info, dict) or not info.get("hasNextPage"):
            return
        next_cursor = info.get("endCursor")
        if not isinstance(next_cursor, str) or not next_cursor:
            raise RuntimeError("Shopify indique une page suivante sans curseur")
        if next_cursor in seen:
            raise RuntimeError("Boucle de pagination Shopify détectée")
        seen.add(next_cursor)
        cursor = next_cursor
    raise RuntimeError(f"Limite de pagination dépassée ({max_pages} pages)")
