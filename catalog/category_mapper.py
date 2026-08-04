from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CategoryMatch:
    source: str
    product_type: str
    confidence: float
    fallback: bool


class CategoryMapper:
    def __init__(self, mapping: dict[str, str] | None = None, keyword_mapping: dict[str, str] | None = None) -> None:
        self.mapping = {str(key): str(value) for key, value in (mapping or {}).items()}
        self.keyword_mapping = {str(key).lower(): str(value) for key, value in (keyword_mapping or {}).items()}

    def shopify_type(self, alibaba_category_id: str, fallback: str = "General") -> str:
        return self.match(alibaba_category_id, fallback=fallback).product_type

    def match(self, alibaba_category_id: str, *, title: str = "", fallback: str = "General") -> CategoryMatch:
        source = str(alibaba_category_id)
        if source in self.mapping:
            return CategoryMatch(source, self.mapping[source], 1.0, False)
        lowered = title.lower()
        matches = [(keyword, target) for keyword, target in self.keyword_mapping.items() if keyword in lowered]
        if matches:
            keyword, target = max(matches, key=lambda item: len(item[0]))
            return CategoryMatch(source, target, min(0.95, 0.55 + len(keyword) / 100), False)
        return CategoryMatch(source, fallback, 0.0, True)
