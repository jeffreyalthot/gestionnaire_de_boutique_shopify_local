from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.paths import PROJECT_ROOT

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_env: Literal["development", "test", "production"] = "development"
    app_name: str = "shopify_alibaba_ai_orchestrator"
    app_host: str = "127.0.0.1"
    app_port: int = Field(8080, ge=1, le=65535)
    app_timezone: str = "America/Montreal"
    app_currency: str = "CAD"
    app_log_level: str = "INFO"
    app_dry_run: bool = True
    app_database_path: Path = Path("data/database/orchestrator.db")
    app_public_base_url: str = "http://127.0.0.1:8080"
    api_mutations_enabled: bool = False
    operator_api_token: SecretStr = SecretStr("")
    api_loopback_only: bool = True

    shopify_shop_domain: str = ""
    shopify_client_id: str = ""
    shopify_client_secret: SecretStr = SecretStr("")
    shopify_admin_access_token: SecretStr = SecretStr("")
    shopify_webhook_secret: SecretStr = SecretStr("")
    shopify_api_version: str = "2026-07"
    shopify_callback_base_url: str = ""
    shopify_enable_rest_compatibility: bool = False
    shopify_request_timeout_seconds: float = Field(30, gt=0, le=120)
    shopify_max_retries: int = Field(5, ge=0, le=10)
    shopify_webhook_max_body_bytes: int = Field(2 * 1024 * 1024, ge=1024, le=16 * 1024 * 1024)

    alibaba_app_key: str = ""
    alibaba_app_secret: SecretStr = SecretStr("")
    alibaba_access_token: SecretStr = SecretStr("")
    alibaba_refresh_token: SecretStr = SecretStr("")
    alibaba_callback_url: str = ""
    alibaba_gateway_url: str = "https://eco.taobao.com/router/rest"
    alibaba_oauth_url: str = "https://oauth.alibaba.com/authorize"
    alibaba_sign_method: Literal["hmac", "md5"] = "hmac"
    alibaba_payment_mode: Literal["authorized_api", "manual"] = "authorized_api"
    alibaba_payment_token_reference: SecretStr = SecretStr("")
    alibaba_require_manual_payment_approval: bool = True
    alibaba_request_timeout_seconds: float = Field(30, gt=0, le=120)
    alibaba_max_retries: int = Field(5, ge=0, le=10)

    # AliExpress configuration (Open Platform v2)
    aliexpress_app_key: str = ""
    aliexpress_app_secret: SecretStr = SecretStr("")
    aliexpress_access_token: SecretStr = SecretStr("")
    aliexpress_refresh_token: SecretStr = SecretStr("")
    aliexpress_callback_url: str = ""
    aliexpress_base_url: str = "https://api-sg.aliexpress.com/rest"
    aliexpress_oauth_authorize_url: str = "https://oauth.aliexpress.com/authorize"
    aliexpress_oauth_token_url: str = "https://oauth.aliexpress.com/token/create"
    aliexpress_oauth_refresh_url: str = "https://oauth.aliexpress.com/token/refresh"
    aliexpress_request_timeout_seconds: float = Field(30, gt=0, le=120)
    aliexpress_max_retries: int = Field(5, ge=0, le=10)
    aliexpress_rate_limit_rps: float = Field(2.0, ge=0.1, le=100.0)

    aliexpress_rate_limit_rps: float = Field(2.0, ge=0.1, le=100.0)

    pricing_mode: Literal["gross_margin", "markup"] = "gross_margin"
    target_gross_margin_percent: float = Field(50, ge=0, lt=100)
    minimum_gross_margin_percent: float = Field(40, ge=0, lt=100)
    shipping_profit_percent: float = Field(0, ge=0, le=100)
    price_rounding_mode: Literal["none", "psychological", "nearest_cent"] = "psychological"
    price_rounding_ending: float = Field(0.99, ge=0, lt=1)
    platform_fee_percent: float = Field(3, ge=0, le=50)
    currency_buffer_percent: float = Field(2, ge=0, le=50)
    refund_reserve_percent: float = Field(2, ge=0, le=50)
    duty_tax_buffer_percent: float = Field(5, ge=0, le=100)

    alibaba_batch_threshold_cad: float = Field(500, gt=0)
    alibaba_batch_max_age_minutes: int = Field(240, ge=1)
    alibaba_batch_max_orders: int = Field(100, ge=1)
    alibaba_batch_max_suppliers: int = Field(20, ge=1)
    alibaba_batch_allow_partial_submission: bool = False
    alibaba_recheck_stock_before_payment: bool = True
    alibaba_recheck_price_before_payment: bool = True
    alibaba_recheck_freight_before_payment: bool = True

    inventory_sync_interval_seconds: int = Field(60, ge=10)
    inventory_low_stock_threshold: int = Field(5, ge=0)
    inventory_safety_stock_quantity: int = Field(2, ge=0)
    inventory_unpublish_when_out_of_stock: bool = True

    dashboard_refresh_seconds: float = Field(5, ge=0.2, le=10)
    runtime_profile: Literal["lite_2gb", "minimal_2gb", "balanced"] = "lite_2gb"
    runtime_max_rss_mb: int = Field(850, ge=256, le=1536)
    runtime_max_cpu_percent: float = Field(75, ge=10, le=100)
    runtime_max_pending_tasks: int = Field(5000, ge=100, le=100000)
    runtime_max_heavy_operations_per_cycle: int = Field(1, ge=0, le=4)
    runtime_media_cache_mb: int = Field(256, ge=32, le=768)
    runtime_cycle_interval_seconds: int = Field(60, ge=10, le=3600)
    automation_enabled: bool = True
    automation_financial_limit_cad: float = Field(1000, ge=0)
    automation_default_mode: Literal["dry_run", "supervised_live"] = "dry_run"
    shopify_reconciliation_interval_seconds: int = Field(300, ge=30)
    alibaba_reconciliation_interval_seconds: int = Field(300, ge=30)
    product_discovery_interval_seconds: int = Field(1800, ge=60)
    product_discovery_keywords: str = "home organization,pet accessories,desk accessories"
    product_discovery_page_size: int = Field(20, ge=1, le=50)
    product_discovery_max_pages: int = Field(3, ge=1, le=10)
    product_discovery_max_candidates: int = Field(100, ge=1, le=500)
    product_minimum_score: float = Field(0.68, ge=0, le=1)
    supplier_minimum_score: float = Field(0.65, ge=0, le=1)
    order_risk_hold_threshold: float = Field(0.50, ge=0, le=1)
    media_max_download_bytes: int = Field(12582912, ge=1048576, le=52428800)
    media_minimum_dimension: int = Field(400, ge=100, le=4000)
    media_maximum_dimension: int = Field(10000, ge=1000, le=20000)
    media_allowed_hosts: str = ""
    customer_service_default_sla_hours: int = Field(24, ge=1, le=168)
    price_sync_interval_seconds: int = Field(900, ge=60)
    tracking_sync_interval_seconds: int = Field(300, ge=30)
    database_backup_interval_seconds: int = Field(21600, ge=300)
    worker_poll_interval_seconds: float = Field(1, ge=0.1)
    max_concurrent_http_requests: int = Field(2, ge=1, le=2)

    ai_enabled: bool = False
    ai_profile: str = "strict_750mb"
    ai_max_ram_mb: int = Field(750, ge=128, le=1000)
    ai_max_cpu_percent: float = Field(65, ge=1, le=100)
    ai_worker_threads: int = Field(1, ge=1, le=2)
    ai_online_learning: bool = False
    ai_micro_llm_enabled: bool = False
    ai_micro_llm_model_path: Path | None = None
    ai_micro_llm_context_size: int = Field(256, ge=64, le=2048)
    ai_minimum_autonomous_confidence: float = Field(0.92, ge=0, le=1)

    secret_storage_provider: str = "windows_dpapi"
    database_encrypt_pii: bool = True
    audit_log_enabled: bool = True
    customer_address_retention_days: int = Field(90, ge=1)
    payment_data_storage_forbidden: bool = True
    master_encryption_key: SecretStr = SecretStr("")

    @field_validator("shopify_shop_domain")
    @classmethod
    def normalize_shop_domain(cls, value: str) -> str:
        return value.removeprefix("https://").removeprefix("http://").rstrip("/")

    @model_validator(mode="after")
    def enforce_security(self) -> "Settings":
        if not self.payment_data_storage_forbidden:
            raise ValueError("PAYMENT_DATA_STORAGE_FORBIDDEN doit rester activé.")
        if self.ai_micro_llm_enabled and not self.ai_micro_llm_model_path:
            raise ValueError("AI_MICRO_LLM_MODEL_PATH est requis lorsque le micro-LLM est activé.")
        if self.api_mutations_enabled and not self.operator_api_token.get_secret_value():
            raise ValueError("OPERATOR_API_TOKEN est requis lorsque API_MUTATIONS_ENABLED est activé.")
        return self

    @property
    def database_path(self) -> Path:
        path = self.app_database_path
        return path if path.is_absolute() else PROJECT_ROOT / path

    @property
    def shopify_graphql_url(self) -> str:
        if not self.shopify_shop_domain:
            return ""
        return f"https://{self.shopify_shop_domain}/admin/api/{self.shopify_api_version}/graphql.json"

    @property
    def live_shopify_ready(self) -> bool:
        return bool(self.shopify_shop_domain and self.shopify_admin_access_token.get_secret_value())

    @property
    def live_alibaba_ready(self) -> bool:
        return bool(self.alibaba_app_key and self.alibaba_app_secret.get_secret_value()
                    and self.alibaba_access_token.get_secret_value())

    @property
    def live_payment_ready(self) -> bool:
        return self.live_alibaba_ready and self.alibaba_payment_mode == "authorized_api"

    @property
    def live_aliexpress_ready(self) -> bool:
        return bool(self.aliexpress_app_key and self.aliexpress_app_secret.get_secret_value()
                    and self.aliexpress_access_token.get_secret_value())

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
