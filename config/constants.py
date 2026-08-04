from __future__ import annotations
from decimal import Decimal

APP_VERSION = "1.0.0"
CAD = "CAD"
ZERO = Decimal("0")
MONEY_QUANTUM = Decimal("0.01")
SHOPIFY_WEBHOOK_ID_HEADER = "X-Shopify-Webhook-Id"
SHOPIFY_HMAC_HEADER = "X-Shopify-Hmac-Sha256"
SHOPIFY_TOPIC_HEADER = "X-Shopify-Topic"
SHOPIFY_SHOP_HEADER = "X-Shopify-Shop-Domain"
