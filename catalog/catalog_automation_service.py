from __future__ import annotations

from decimal import Decimal
from typing import Any

from catalog.discovery.candidate_deduplicator import CandidateDeduplicator
from catalog.discovery.candidate_repository import CandidateRepository
from catalog.discovery.product_candidate import ProductCandidate
from catalog.discovery.search_plan import SearchPlan
from catalog.intelligence.product_ranker import ProductRanker
from catalog.import_pipeline import ProductImportPipeline


class CatalogAutomationService:
    """Chemin canonique Alibaba -> qualification -> préparation Shopify."""

    def __init__(self, container: Any) -> None:
        self.container = container
        self.deduplicator = CandidateDeduplicator()
        self.ranker = ProductRanker()
        self.repository = CandidateRepository(container.db)
        self.importer = ProductImportPipeline(container.pricing, container.currency)

    @staticmethod
    def _items(payload: dict[str, Any]) -> list[dict[str, Any]]:
        for key in ("products", "items", "result", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
            if isinstance(value, dict):
                nested = value.get("products") or value.get("items") or value.get("list")
                if isinstance(nested, list):
                    return [item for item in nested if isinstance(item, dict)]
        return []

    @staticmethod
    def _candidate(raw: dict[str, Any]) -> ProductCandidate:
        identifier = str(raw.get("product_id") or raw.get("productId") or raw.get("id") or "")
        if not identifier:
            raise ValueError("Produit Alibaba sans identifiant")
        supplier = raw.get("supplier") if isinstance(raw.get("supplier"), dict) else {}
        images = raw.get("images") or raw.get("image_urls") or []
        if isinstance(images, str):
            images = [images]
        return ProductCandidate(
            source_id=identifier,
            title=str(raw.get("title") or raw.get("subject") or "Produit sans titre"),
            supplier_id=str(raw.get("supplier_id") or supplier.get("id") or ""),
            category_id=str(raw.get("category_id") or raw.get("categoryId") or ""),
            currency=str(raw.get("currency") or "USD"),
            unit_cost=float(raw.get("price") or raw.get("unit_price") or 0),
            min_order_quantity=max(1, int(raw.get("min_order_quantity") or raw.get("moq") or 1)),
            image_urls=tuple(str(url) for url in images if url),
            signals={
                "demand": float(raw.get("demand_score", .5) or .5),
                "margin": float(raw.get("margin_score", .5) or .5),
                "supplier": float(raw.get("supplier_score", .5) or .5),
                "quality": float(raw.get("quality_score", .5) or .5),
                "shipping": float(raw.get("shipping_score", .5) or .5),
                "competition": float(raw.get("competition_score", .5) or .5),
                "return_risk": float(raw.get("return_risk", .2) or .2),
            },
            raw=raw,
        )

    async def discover(self, plan: SearchPlan) -> dict[str, Any]:
        plan.validate()
        candidates: list[ProductCandidate] = []
        pages = 0
        for query in plan.queries:
            for page in range(1, plan.max_pages + 1):
                pages += 1
                payload = await self.container.alibaba.search_distribution_products(query, page=page, page_size=plan.page_size)
                items = self._items(payload)
                candidates.extend(self._candidate(item) for item in items)
                if len(items) < plan.page_size or len(candidates) >= plan.max_candidates:
                    break
            if len(candidates) >= plan.max_candidates:
                break
        unique = self.deduplicator.unique(candidates)[: plan.max_candidates]
        ranked = self.ranker.rank(unique, limit=plan.max_candidates)
        for item in ranked:
            self.repository.save(item.candidate, score=item.score)
        return {"queries": len(plan.queries), "pages": pages, "candidates": len(candidates), "unique": len(unique), "ranked": [{"id": item.candidate.source_id, "score": item.score} for item in ranked]}

    async def prepare_for_shopify(self, raw: dict[str, Any], shipping_cost: Decimal) -> dict[str, Any]:
        return await self.importer.prepare(raw, shipping_cost)
