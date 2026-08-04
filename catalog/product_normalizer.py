from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal
from typing import Any

from catalog.title_generator import generate_title
from integrations.alibaba.mappers.product_mapper import map_alibaba_product


@dataclass(frozen=True, slots=True)
class NormalizationReport:
    product: dict[str, object]
    warnings: tuple[str, ...]
    valid: bool

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class ProductNormalizer:
    def normalize(self, payload: dict[str, object]) -> dict[str, object]:
        return self.normalize_with_report(payload).product

    def normalize_with_report(self, payload: dict[str, object]) -> NormalizationReport:
        if not isinstance(payload, dict):
            raise TypeError("payload must be a dict")
        product = dict(map_alibaba_product(payload))
        warnings: list[str] = []
        product["title"] = generate_title(str(product.get("title", payload.get("subject", ""))))
        if not product["title"]:
            warnings.append("missing_title")
        product_id = str(product.get("supplier_product_id", product.get("id", "")))
        if not product_id:
            warnings.append("missing_supplier_product_id")
        product["supplier_product_id"] = product_id
        try:
            price = Decimal(str(product.get("supplier_cost", product.get("price", 0)) or 0))
        except Exception:
            price = Decimal("0"); warnings.append("invalid_price")
        product["supplier_cost"] = price
        stock = int(product.get("stock", 0) or 0)
        product["stock"] = max(0, stock)
        if stock < 0:
            warnings.append("negative_stock_clamped")
        images = product.get("images") or []
        product["images"] = list(dict.fromkeys(str(url) for url in images if str(url).strip())) if isinstance(images, list) else []
        if not product["images"]:
            warnings.append("missing_images")
        return NormalizationReport(product, tuple(warnings), not {"missing_title", "missing_supplier_product_id", "invalid_price"}.intersection(warnings))
