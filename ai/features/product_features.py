from __future__ import annotations

from ai.features.base import as_float, bounded, safe_ratio


def product_features(product: dict[str, object]) -> dict[str, float]:
    price = max(0.0, as_float(product.get("sale_price_cad")))
    landed = max(0.0, as_float(product.get("landed_cost_cad")))
    stock = max(0.0, as_float(product.get("stock")))
    sales = max(0.0, as_float(product.get("sales_30d")))
    returns = max(0.0, as_float(product.get("returns_30d")))
    return {
        "price": price,
        "landed_cost": landed,
        "margin": bounded(product.get("margin_percent", safe_ratio(price - landed, price) * 100.0), 0.0, 100.0) / 100.0,
        "markup": max(0.0, safe_ratio(price - landed, landed)),
        "stock": min(1.0, stock / max(1.0, as_float(product.get("stock_normalizer", 100.0)))),
        "stock_days": max(0.0, safe_ratio(stock, max(1.0, sales / 30.0))),
        "quality": bounded(product.get("score", product.get("quality_score", 0.0))),
        "return_rate": bounded(safe_ratio(returns, sales)),
        "supplier_score": bounded(product.get("supplier_score", 0.0)),
        "media_count": max(0.0, as_float(product.get("media_count"))),
    }
