# Index complet des modules, classes et fonctions

Cet index est généré depuis l’AST Python de la livraison. Il sert de référence pour les imports et l’évolution du projet.

## `ai/agents/accounting_agent.py`
- Classe `AccountingAgent`
  - Méthodes : `decide`

## `ai/agents/anomaly_agent.py`
- Classe `AnomalyAgent`
  - Méthodes : `decide`

## `ai/agents/compliance_agent.py`
- Classe `ComplianceAgent`
  - Méthodes : `decide`

## `ai/agents/customer_service_agent.py`
- Classe `CustomerServiceAgent`
  - Méthodes : `decide`

## `ai/agents/demand_agent.py`
- Classe `DemandAgent`
  - Méthodes : `decide`

## `ai/agents/inventory_agent.py`
- Classe `InventoryAgent`
  - Méthodes : `decide`

## `ai/agents/order_risk_agent.py`
- Classe `OrderRiskAgent`
  - Méthodes : `decide`

## `ai/agents/pricing_agent.py`
- Classe `PricingAgent`
  - Méthodes : `decide`

## `ai/agents/procurement_agent.py`
- Classe `ProcurementAgent`
  - Méthodes : `decide`

## `ai/agents/product_quality_agent.py`
- Classe `ProductQualityAgent`
  - Méthodes : `decide`

## `ai/agents/product_scout_agent.py`
- Classe `ProductScoutAgent`
  - Méthodes : `decide`

## `ai/agents/shipping_agent.py`
- Classe `ShippingAgent`
  - Méthodes : `decide`

## `ai/agents/supervisor_agent.py`
- Classe `SupervisorAgent`
  - Méthodes : `decide`

## `ai/agents/supplier_risk_agent.py`
- Classe `SupplierRiskAgent`
  - Méthodes : `decide`

## `ai/features/customer_features.py`
- Fonctions : `customer_features`

## `ai/features/feature_store.py`
- Classe `FeatureStore`
  - Méthodes : `__init__`, `set`, `get`

## `ai/features/order_features.py`
- Fonctions : `order_features`

## `ai/features/pricing_features.py`
- Fonctions : `pricing_features`

## `ai/features/product_features.py`
- Fonctions : `product_features`

## `ai/features/shipping_features.py`
- Fonctions : `shipping_features`

## `ai/features/supplier_features.py`
- Fonctions : `supplier_features`

## `ai/language/customer_reply_generator.py`
- Classe `CustomerReplyGenerator`
  - Méthodes : `tracking`, `delay`

## `ai/language/optional_llama_cpp_adapter.py`
- Classe `OptionalLlamaCppAdapter`
  - Méthodes : `__init__`, `complete`

## `ai/language/product_copy_generator.py`
- Classe `ProductCopyGenerator`
  - Méthodes : `generate`

## `ai/language/template_engine.py`
- Classe `TemplateEngine`
  - Méthodes : `render`

## `ai/language/text_sanitizer.py`
- Fonctions : `sanitize`

## `ai/language/translation_adapter.py`
- Classe `TranslationAdapter`
  - Méthodes : `translate`

## `ai/memory/decision_history.py`
- Classe `DecisionHistory`
  - Méthodes : `put`, `get`

## `ai/memory/error_memory.py`
- Classe `ErrorMemory`
  - Méthodes : `put`, `get`

## `ai/memory/long_term_memory.py`
- Classe `LongTermMemory`
  - Méthodes : `__init__`, `remember`, `recall`

## `ai/memory/product_memory.py`
- Classe `ProductMemory`
  - Méthodes : `put`, `get`

## `ai/memory/short_term_memory.py`
- Classe `ShortTermMemory`
  - Méthodes : `__init__`, `add`, `recent`

## `ai/memory/supplier_memory.py`
- Classe `SupplierMemory`
  - Méthodes : `put`, `get`

## `ai/models/anomaly_detector.py`
- Classe `OnlineAnomalyDetector`
  - Méthodes : `__init__`, `partial_fit`, `is_anomaly`

## `ai/models/contextual_bandit.py`
- Classe `ContextualBandit`
  - Méthodes : `__init__`, `choose`, `update`

## `ai/models/conversion_predictor.py`
- Classe `ConversionPredictor`
  - Méthodes : `__init__`

## `ai/models/demand_forecaster.py`
- Classe `DemandForecaster`
  - Méthodes : `features`

## `ai/models/online_classifier.py`
- Classe `OnlineTextClassifier`
  - Méthodes : `__init__`, `partial_fit`, `predict`

## `ai/models/online_regressor.py`
- Classe `OnlineRegressor`
  - Méthodes : `__init__`, `partial_fit`, `predict`

## `ai/models/product_ranker.py`
- Fonctions : `product_rank`

## `ai/models/return_probability_model.py`
- Classe `ReturnProbabilityModel`
  - Méthodes : `probability`

## `ai/models/shipping_delay_model.py`
- Classe `ShippingDelayModel`
  - Méthodes : `expected_days`

## `ai/models/supplier_risk_model.py`
- Fonctions : `supplier_risk`

## `ai/models/text_category_model.py`
- Classe `TextCategoryModel`
  - Méthodes : `__init__`

## `ai/policies/autonomy_policy.py`
- Fonctions : `may_execute`

## `ai/policies/confidence_policy.py`
- Fonctions : `autonomous`

## `ai/policies/financial_action_policy.py`
- Fonctions : `financial_action_allowed`

## `ai/policies/human_approval_policy.py`
- Fonctions : `requires_approval`

## `ai/policies/safe_action_policy.py`
- Fonctions : `safe_action`

## `ai/runtime/ai_runtime.py`
- Classe `AIRuntime`
  - Méthodes : `__init__`, `status`, `score_product`, `score_supplier`, `_record`

## `ai/runtime/cpu_budget.py`
- Classe `CPUBudget`
  - Méthodes : `__init__`, `current`, `overloaded`

## `ai/runtime/fallback_engine.py`
- Classe `FallbackEngine`
  - Méthodes : `classify`

## `ai/runtime/inference_scheduler.py`
- Classe `InferenceScheduler`
  - Méthodes : `__init__`, `run`

## `ai/runtime/memory_budget.py`
- Classe `MemorySnapshot`
- Classe `MemoryBudget`
  - Méthodes : `__init__`, `snapshot`, `require`

## `ai/runtime/model_loader.py`
- Fonctions : `load_model`

## `ai/runtime/model_registry.py`
- Classe `ModelRegistry`
  - Méthodes : `__init__`, `register`, `get`, `unload`, `names`

## `ai/runtime/model_unloader.py`
- Fonctions : `unload_reference`

## `ai/runtime/resource_guard.py`
- Classe `ResourceGuard`
  - Méthodes : `__init__`, `inference`

## `ai/training/checkpoint_manager.py`
- Classe `CheckpointManager`
  - Méthodes : `save`, `load`

## `ai/training/drift_detector.py`
- Classe `DriftDetector`
  - Méthodes : `__init__`, `update`

## `ai/training/evaluation.py`
- Fonctions : `binary_metrics`

## `ai/training/feedback_collector.py`
- Classe `FeedbackCollector`
  - Méthodes : `__init__`, `record`

## `ai/training/online_trainer.py`
- Classe `OnlineTrainer`
  - Méthodes : `__init__`, `train_text`

## `ai/training/rollback_manager.py`
- Fonctions : `rollback_model`

## `api/dependencies.py`
- Fonctions : `get_container`

## `api/exception_handlers.py`
- Fonctions : `unhandled_exception_handler`

## `api/middleware/body_size_limit.py`
- Classe `BodySizeLimitMiddleware`
  - Méthodes : `__init__`, `dispatch`

## `api/middleware/exception_guard.py`
- Classe `ExceptionGuardMiddleware`
  - Méthodes : `dispatch`

## `api/middleware/rate_limiter.py`
- Classe `RateLimiterMiddleware`
  - Méthodes : `__init__`, `dispatch`

## `api/middleware/request_id.py`
- Classe `RequestIdMiddleware`
  - Méthodes : `dispatch`

## `api/middleware/request_logging.py`
- Classe `RequestLoggingMiddleware`
  - Méthodes : `dispatch`

## `api/middleware/security_headers.py`
- Classe `SecurityHeadersMiddleware`
  - Méthodes : `dispatch`

## `api/request_context.py`
- Classe `RequestContext`

## `api/router.py`
- Fonctions : `build_router`

## `api/routes/alibaba_oauth.py`
- Fonctions : `router_for`

## `api/routes/configuration.py`
- Fonctions : `router_for`

## `api/routes/dashboard_data.py`
- Fonctions : `router_for`

## `api/routes/health.py`
- Fonctions : `router_for`

## `api/routes/manual_approvals.py`
- Classe `Decision`
- Fonctions : `router_for`

## `api/routes/metrics.py`
- Fonctions : `router_for`

## `api/routes/shopify_carrier_rates.py`
- Fonctions : `router_for`

## `api/routes/shopify_oauth.py`
- Fonctions : `router_for`

## `api/routes/status.py`
- Fonctions : `router_for`

## `api/schemas/approvals.py`
- Classe `ApprovalDecision`

## `api/schemas/dashboard.py`
- Classe `DashboardResponse`

## `api/schemas/health.py`
- Classe `HealthResponse`

## `api/schemas/oauth.py`
- Classe `OAuthStartResponse`

## `api/schemas/shipping.py`
- Classe `ShippingRate`

## `api/schemas/webhooks.py`
- Classe `WebhookReceipt`

## `api/server.py`
- Fonctions : `create_app`

## `app/application.py`
- Classe `Application`
  - Méthodes : `__init__`, `_build_worker`, `_build_scheduler`, `run_once`, `run`, `stop`

## `app/bootstrap.py`
- Fonctions : `bootstrap`

## `app/dependency_container.py`
- Classe `Container`
  - Méthodes : `dashboard_state`, `status`, `close`
- Fonctions : `build_container`

## `app/graceful_shutdown.py`
- Fonctions : `cancel_tasks`

## `app/lifecycle.py`
- Fonctions : `install_signal_handlers`

## `app/liveness.py`
- Fonctions : `liveness`

## `app/readiness.py`
- Fonctions : `readiness`

## `app/startup_checks.py`
- Fonctions : `run_startup_checks`

## `catalog/attribute_mapper.py`
- Fonctions : `option_definitions`

## `catalog/catalog_sync.py`
- Classe `CatalogSync`
  - Méthodes : `__init__`, `schedule`

## `catalog/category_mapper.py`
- Classe `CategoryMapper`
  - Méthodes : `__init__`, `shopify_type`

## `catalog/description_generator.py`
- Fonctions : `generate_description`

## `catalog/discovery_engine.py`
- Classe `ProductDiscoveryEngine`
  - Méthodes : `__init__`, `discover`

## `catalog/duplicate_detector.py`
- Classe `DuplicateDetector`
  - Méthodes : `similar`

## `catalog/image_pipeline.py`
- Fonctions : `shopify_files`

## `catalog/image_validator.py`
- Fonctions : `valid_image_urls`

## `catalog/import_pipeline.py`
- Classe `ProductImportPipeline`
  - Méthodes : `__init__`, `prepare`

## `catalog/product_eligibility.py`
- Fonctions : `eligibility`

## `catalog/product_normalizer.py`
- Classe `ProductNormalizer`
  - Méthodes : `normalize`

## `catalog/publishing_policy.py`
- Fonctions : `should_publish`

## `catalog/quality_score.py`
- Fonctions : `quality_score`

## `catalog/seo_generator.py`
- Fonctions : `seo_fields`

## `catalog/supplier_score.py`
- Fonctions : `supplier_score`

## `catalog/tag_generator.py`
- Fonctions : `generate_tags`

## `catalog/title_generator.py`
- Fonctions : `generate_title`

## `catalog/variant_normalizer.py`
- Fonctions : `normalize_variants`

## `cli/ai_commands.py`
- Classe `AiCommands`
  - Méthodes : `__init__`, `execute`

## `cli/approval_commands.py`
- Classe `ApprovalCommands`
  - Méthodes : `__init__`, `execute`

## `cli/batch_commands.py`
- Classe `BatchCommands`
  - Méthodes : `__init__`, `execute`

## `cli/command_router.py`
- Classe `CommandRouter`
  - Méthodes : `__init__`, `register`, `execute`

## `cli/emergency_commands.py`
- Classe `EmergencyCommands`
  - Méthodes : `__init__`, `execute`

## `cli/interactive_shell.py`
- Classe `InteractiveShell`
  - Méthodes : `__init__`, `display`

## `cli/inventory_commands.py`
- Classe `InventoryCommands`
  - Méthodes : `__init__`, `execute`

## `cli/maintenance_commands.py`
- Classe `MaintenanceCommands`
  - Méthodes : `__init__`, `execute`

## `cli/menu_renderer.py`
- Classe `MenuRenderer`
  - Méthodes : `__init__`, `show`

## `cli/order_commands.py`
- Classe `OrderCommands`
  - Méthodes : `__init__`, `execute`

## `cli/payment_commands.py`
- Classe `PaymentCommands`
  - Méthodes : `__init__`, `execute`

## `cli/product_commands.py`
- Classe `ProductCommands`
  - Méthodes : `__init__`, `execute`

## `cli/reconciliation_commands.py`
- Classe `ReconciliationCommands`
  - Méthodes : `__init__`, `execute`

## `cli/status_commands.py`
- Classe `StatusCommands`
  - Méthodes : `__init__`, `execute`

## `compliance/compliance_report.py`
- Fonctions : `compliance_summary`

## `compliance/counterfeit_risk_filter.py`
- Fonctions : `counterfeit_risk`

## `compliance/country_restriction_filter.py`
- Fonctions : `country_allowed`

## `compliance/customer_data_retention.py`
- Fonctions : `purge_expired_addresses`

## `compliance/customs_compliance.py`
- Fonctions : `customs_fields`

## `compliance/dangerous_goods_filter.py`
- Fonctions : `dangerous_goods_reason`

## `compliance/privacy_compliance.py`
- Fonctions : `minimize_payload`

## `compliance/restricted_product_filter.py`
- Fonctions : `restricted_reason`

## `compliance/tax_compliance.py`
- Fonctions : `tax_registration_required`

## `compliance/trademark_filter.py`
- Fonctions : `contains_protected_brand`

## `config/env_schema.py`
- Classe `CredentialStatus`

## `config/feature_flags.py`
- Classe `FeatureFlags`

## `config/paths.py`
- Fonctions : `ensure_runtime_directories`

## `config/settings.py`
- Classe `Settings`
  - Méthodes : `normalize_shop_domain`, `enforce_security`, `database_path`, `shopify_graphql_url`, `live_shopify_ready`, `live_alibaba_ready`, `live_payment_ready`
- Fonctions : `get_settings`

## `dashboard/dashboard_controller.py`
- Classe `DashboardController`
  - Méthodes : `__init__`, `snapshot`

## `dashboard/dashboard_state.py`
- Classe `DashboardState`
  - Méthodes : `uptime_seconds`

## `dashboard/formatter.py`
- Fonctions : `duration`, `money`

## `dashboard/keyboard_handler.py`
- Classe `KeyboardHandler`
  - Méthodes : `action`

## `dashboard/live_dashboard.py`
- Classe `LiveDashboard`
  - Méthodes : `__init__`, `render`, `run`, `stop`

## `dashboard/panels/activity_log_panel.py`
- Classe `ActivityLogPanel`
  - Méthodes : `render`

## `dashboard/panels/ai_panel.py`
- Classe `AiPanel`
  - Méthodes : `render`

## `dashboard/panels/alerts_panel.py`
- Classe `AlertsPanel`
  - Méthodes : `render`

## `dashboard/panels/api_health_panel.py`
- Classe `ApiHealthPanel`
  - Méthodes : `render`

## `dashboard/panels/cashflow_panel.py`
- Classe `CashflowPanel`
  - Méthodes : `render`

## `dashboard/panels/expenses_panel.py`
- Classe `ExpensesPanel`
  - Méthodes : `render`

## `dashboard/panels/header_panel.py`
- Classe `HeaderPanel`
  - Méthodes : `render`

## `dashboard/panels/inventory_panel.py`
- Classe `InventoryPanel`
  - Méthodes : `render`

## `dashboard/panels/orders_panel.py`
- Classe `OrdersPanel`
  - Méthodes : `render`

## `dashboard/panels/payments_panel.py`
- Classe `PaymentsPanel`
  - Méthodes : `render`

## `dashboard/panels/procurement_panel.py`
- Classe `ProcurementPanel`
  - Méthodes : `render`

## `dashboard/panels/profit_panel.py`
- Classe `ProfitPanel`
  - Méthodes : `render`

## `dashboard/panels/refunds_panel.py`
- Classe `RefundsPanel`
  - Méthodes : `render`

## `dashboard/panels/resource_panel.py`
- Classe `ResourcePanel`
  - Méthodes : `render`

## `dashboard/panels/revenue_panel.py`
- Classe `RevenuePanel`
  - Méthodes : `render`

## `dashboard/panels/runtime_panel.py`
- Classe `RuntimePanel`
  - Méthodes : `render`

## `dashboard/panels/shipping_panel.py`
- Classe `ShippingPanel`
  - Méthodes : `render`

## `dashboard/refresh_loop.py`
- Fonctions : `refresh_loop`

## `domain/entities/ai_decision.py`
- Classe `AIDecision`

## `domain/entities/api_event.py`
- Classe `ApiEvent`

## `domain/entities/audit_event.py`
- Classe `AuditEvent`

## `domain/entities/customer.py`
- Classe `Customer`

## `domain/entities/customer_address.py`
- Classe `CustomerAddress`

## `domain/entities/expense.py`
- Classe `Expense`

## `domain/entities/fulfillment.py`
- Classe `Fulfillment`

## `domain/entities/inventory_item.py`
- Classe `InventoryItem`

## `domain/entities/inventory_snapshot.py`
- Classe `InventorySnapshot`

## `domain/entities/ledger_entry.py`
- Classe `LedgerEntry`

## `domain/entities/manual_approval.py`
- Classe `ManualApproval`

## `domain/entities/payment.py`
- Classe `Payment`

## `domain/entities/payment_attempt.py`
- Classe `PaymentAttempt`

## `domain/entities/procurement_batch.py`
- Classe `ProcurementBatch`

## `domain/entities/product.py`
- Classe `Product`

## `domain/entities/product_category.py`
- Classe `ProductCategory`

## `domain/entities/product_media.py`
- Classe `ProductMedia`

## `domain/entities/product_variant.py`
- Classe `ProductVariant`

## `domain/entities/profit_snapshot.py`
- Classe `ProfitSnapshot`

## `domain/entities/reconciliation_checkpoint.py`
- Classe `ReconciliationCheckpoint`

## `domain/entities/refund.py`
- Classe `Refund`

## `domain/entities/return_request.py`
- Classe `ReturnRequest`

## `domain/entities/shipment.py`
- Classe `Shipment`

## `domain/entities/shipping_quote.py`
- Classe `ShippingQuote`

## `domain/entities/shop.py`
- Classe `Shop`

## `domain/entities/shopify_order.py`
- Classe `ShopifyOrder`

## `domain/entities/shopify_order_line.py`
- Classe `ShopifyOrderLine`

## `domain/entities/supplier.py`
- Classe `Supplier`

## `domain/entities/supplier_offer.py`
- Classe `SupplierOffer`

## `domain/entities/supplier_order.py`
- Classe `SupplierOrder`

## `domain/entities/supplier_order_line.py`
- Classe `SupplierOrderLine`

## `domain/entities/tracking_event.py`
- Classe `TrackingEvent`

## `domain/enums/approval_status.py`
- Classe `ApprovalStatus`

## `domain/enums/batch_status.py`
- Classe `BatchStatus`

## `domain/enums/decision_type.py`
- Classe `DecisionType`

## `domain/enums/fulfillment_status.py`
- Classe `FulfillmentStatus`

## `domain/enums/order_status.py`
- Classe `OrderStatus`

## `domain/enums/payment_status.py`
- Classe `PaymentStatus`

## `domain/enums/product_status.py`
- Classe `ProductStatus`

## `domain/enums/risk_level.py`
- Classe `RiskLevel`

## `domain/enums/shipment_status.py`
- Classe `ShipmentStatus`

## `domain/enums/supplier_status.py`
- Classe `SupplierStatus`

## `domain/events/ai_events.py`
- Fonctions : `ai_event`

## `domain/events/base_event.py`
- Classe `DomainEvent`

## `domain/events/inventory_events.py`
- Fonctions : `inventory_event`

## `domain/events/order_events.py`
- Fonctions : `order_event`

## `domain/events/payment_events.py`
- Fonctions : `payment_event`

## `domain/events/procurement_events.py`
- Fonctions : `procurement_event`

## `domain/events/product_events.py`
- Fonctions : `product_event`

## `domain/events/shipping_events.py`
- Fonctions : `shipping_event`

## `domain/services/batching_service.py`
- Fonctions : `threshold_reached`

## `domain/services/inventory_service.py`
- Fonctions : `sellable_stock`

## `domain/services/order_validation_service.py`
- Fonctions : `validate_paid_order`

## `domain/services/profit_service.py`
- Fonctions : `profit`

## `domain/services/refund_service.py`
- Fonctions : `refundable_amount`

## `domain/services/risk_service.py`
- Fonctions : `risk_level`

## `domain/services/shipping_service.py`
- Fonctions : `choose_shipping_option`

## `domain/state_machines/base.py`
- Classe `Transition`
- Classe `StateMachine`
  - Méthodes : `__init__`, `transition`

## `domain/state_machines/fulfillment_state_machine.py`
- Classe `FulfillmentStateMachine`
  - Méthodes : `__init__`

## `domain/state_machines/payment_state_machine.py`
- Classe `PaymentStateMachine`
  - Méthodes : `__init__`

## `domain/state_machines/procurement_batch_state_machine.py`
- Classe `ProcurementBatchStateMachine`
  - Méthodes : `__init__`

## `domain/state_machines/return_state_machine.py`
- Classe `ReturnStateMachine`
  - Méthodes : `__init__`

## `domain/state_machines/shopify_order_state_machine.py`
- Classe `ShopifyOrderStateMachine`
  - Méthodes : `__init__`

## `domain/state_machines/supplier_order_state_machine.py`
- Classe `SupplierOrderStateMachine`
  - Méthodes : `__init__`

## `domain/value_objects/address.py`
- Classe `Address`
  - Méthodes : `validate`, `as_supplier_payload`

## `domain/value_objects/barcode.py`
- Classe `Barcode`
  - Méthodes : `__post_init__`

## `domain/value_objects/country_code.py`
- Classe `CountryCode`
  - Méthodes : `__post_init__`

## `domain/value_objects/currency_code.py`
- Classe `CurrencyCode`
  - Méthodes : `__post_init__`

## `domain/value_objects/date_range.py`
- Classe `DateRange`
  - Méthodes : `__post_init__`

## `domain/value_objects/dimensions.py`
- Classe `Dimensions`
  - Méthodes : `volume_cm3`

## `domain/value_objects/external_id.py`
- Classe `ExternalId`
  - Méthodes : `__post_init__`

## `domain/value_objects/idempotency_key.py`
- Fonctions : `build_idempotency_key`

## `domain/value_objects/money.py`
- Classe `Money`
  - Méthodes : `__post_init__`, `__add__`, `__sub__`, `__mul__`, `_same_currency`, `as_float`, `as_dict`

## `domain/value_objects/percentage.py`
- Classe `Percentage`
  - Méthodes : `__post_init__`, `ratio`

## `domain/value_objects/quantity.py`
- Classe `Quantity`
  - Méthodes : `__post_init__`

## `domain/value_objects/sku.py`
- Classe `SKU`
  - Méthodes : `__post_init__`

## `domain/value_objects/weight.py`
- Classe `Weight`
  - Méthodes : `__post_init__`

## `finance/accounting_engine.py`
- Classe `AccountingEngine`
  - Méthodes : `__init__`, `recognize_sale`, `recognize_supplier_cost`, `recognize_shipping`, `recognize_refund`

## `finance/currency_gain_loss.py`
- Fonctions : `currency_gain_loss`

## `finance/daily_close.py`
- Fonctions : `daily_close`

## `finance/double_entry_ledger.py`
- Classe `DoubleEntryLedger`
  - Méthodes : `__init__`, `post`, `balanced`

## `finance/expense_recognizer.py`
- Fonctions : `recognize_procurement`

## `finance/financial_snapshot.py`
- Fonctions : `snapshot`

## `finance/gross_profit_calculator.py`
- Fonctions : `gross_profit`

## `finance/liability_calculator.py`
- Fonctions : `outstanding_supplier_liability`

## `finance/monthly_close.py`
- Fonctions : `monthly_close`

## `finance/net_profit_calculator.py`
- Fonctions : `net_profit`

## `finance/payout_reconciler.py`
- Fonctions : `reconcile_payout`

## `finance/refund_reserve.py`
- Fonctions : `reserve_amount`

## `finance/revenue_recognizer.py`
- Fonctions : `recognize_paid_order`

## `finance/shipping_variance.py`
- Fonctions : `shipping_variance`

## `fulfillment/address_validator.py`
- Fonctions : `validate_shipping_address`

## `fulfillment/customs_data_builder.py`
- Fonctions : `build_customs_line`

## `fulfillment/delivery_exception_handler.py`
- Fonctions : `record_delivery_exception`

## `fulfillment/delivery_option_selector.py`
- Fonctions : `select_option`

## `fulfillment/fulfillment_sync.py`
- Classe `FulfillmentSync`
  - Méthodes : `__init__`, `execute`

## `fulfillment/late_shipment_detector.py`
- Fonctions : `is_late`

## `fulfillment/shipment_monitor.py`
- Classe `ShipmentMonitor`
  - Méthodes : `__init__`, `pending`

## `fulfillment/shipping_quote_cache.py`
- Classe `ShippingQuoteCache`
  - Méthodes : `key`

## `fulfillment/shipping_quote_engine.py`
- Classe `ShippingQuoteEngine`
  - Méthodes : `__init__`, `quote`

## `fulfillment/tracking_sync.py`
- Classe `TrackingSync`
  - Méthodes : `__init__`, `sync`

## `infrastructure/cache/cache_keys.py`
- Fonctions : `cache_key`

## `infrastructure/cache/memory_cache.py`
- Classe `MemoryCache`
  - Méthodes : `__init__`, `set`, `get`, `clear`

## `infrastructure/cache/sqlite_cache.py`
- Classe `SQLiteCache`
  - Méthodes : `__init__`, `set`, `get`

## `infrastructure/database/backup.py`
- Fonctions : `backup_database`

## `infrastructure/database/engine.py`
- Classe `Database`
  - Méthodes : `__init__`, `connect`, `initialize`, `transaction`, `execute`, `query`, `query_one`, `scalar`, `set_value`, `get_value`, `insert_event`, `mark_event`, `insert_audit`, `health`, `financial_snapshot`, `counts`, `purge_expired_leases`
- Fonctions : `utcnow`

## `infrastructure/database/health_check.py`
- Fonctions : `check_database`

## `infrastructure/database/models/ai_decision.py`
- Classe `AiDecisionRecord`

## `infrastructure/database/models/ai_memory.py`
- Classe `AiMemoryRecord`

## `infrastructure/database/models/approval.py`
- Classe `ApprovalRecord`

## `infrastructure/database/models/audit.py`
- Classe `AuditRecord`

## `infrastructure/database/models/customer.py`
- Classe `CustomerRecord`

## `infrastructure/database/models/event.py`
- Classe `EventRecord`

## `infrastructure/database/models/inventory.py`
- Classe `InventoryRecord`

## `infrastructure/database/models/ledger.py`
- Classe `LedgerRecord`

## `infrastructure/database/models/order.py`
- Classe `OrderRecord`

## `infrastructure/database/models/payment.py`
- Classe `PaymentRecord`

## `infrastructure/database/models/procurement_batch.py`
- Classe `ProcurementBatchRecord`

## `infrastructure/database/models/product.py`
- Classe `ProductRecord`

## `infrastructure/database/models/product_mapping.py`
- Classe `ProductMappingRecord`

## `infrastructure/database/models/refund.py`
- Classe `RefundRecord`

## `infrastructure/database/models/shipment.py`
- Classe `ShipmentRecord`

## `infrastructure/database/models/shop.py`
- Classe `ShopRecord`

## `infrastructure/database/models/supplier.py`
- Classe `SupplierRecord`

## `infrastructure/database/models/supplier_order.py`
- Classe `SupplierOrderRecord`

## `infrastructure/database/models/task.py`
- Classe `TaskRecord`

## `infrastructure/database/models/tracking.py`
- Classe `TrackingRecord`

## `infrastructure/database/repositories/ai_repository.py`
- Classe `AiRepository`
  - Méthodes : `__init__`, `get`, `all`, `delete`

## `infrastructure/database/repositories/audit_repository.py`
- Classe `AuditRepository`
  - Méthodes : `__init__`, `get`, `all`, `delete`

## `infrastructure/database/repositories/batch_repository.py`
- Classe `BatchRepository`
  - Méthodes : `__init__`, `get`, `all`, `delete`

## `infrastructure/database/repositories/event_repository.py`
- Classe `EventRepository`
  - Méthodes : `__init__`, `get`, `all`, `delete`

## `infrastructure/database/repositories/inventory_repository.py`
- Classe `InventoryRepository`
  - Méthodes : `__init__`, `get`, `all`, `delete`

## `infrastructure/database/repositories/ledger_repository.py`
- Classe `LedgerRepository`
  - Méthodes : `__init__`, `get`, `all`, `delete`

## `infrastructure/database/repositories/order_repository.py`
- Classe `OrderRepository`
  - Méthodes : `__init__`, `get`, `all`, `delete`

## `infrastructure/database/repositories/payment_repository.py`
- Classe `PaymentRepository`
  - Méthodes : `__init__`, `get`, `all`, `delete`

## `infrastructure/database/repositories/product_repository.py`
- Classe `ProductRepository`
  - Méthodes : `__init__`, `get`, `all`, `delete`

## `infrastructure/database/repositories/shipment_repository.py`
- Classe `ShipmentRepository`
  - Méthodes : `__init__`, `get`, `all`, `delete`

## `infrastructure/database/repositories/supplier_repository.py`
- Classe `SupplierRepository`
  - Méthodes : `__init__`, `get`, `all`, `delete`

## `infrastructure/database/repositories/task_repository.py`
- Classe `TaskRepository`
  - Méthodes : `__init__`, `get`, `all`, `delete`

## `infrastructure/database/restore.py`
- Fonctions : `restore_database`

## `infrastructure/database/session.py`
- Fonctions : `database_session`

## `infrastructure/database/unit_of_work.py`
- Classe `UnitOfWork`
  - Méthodes : `__init__`, `__enter__`, `__exit__`

## `infrastructure/http/async_client.py`
- Fonctions : `create_async_client`

## `infrastructure/http/backoff.py`
- Fonctions : `exponential_backoff`

## `infrastructure/http/circuit_breaker.py`
- Classe `CircuitBreaker`
  - Méthodes : `__init__`, `allow`, `success`, `failure`

## `infrastructure/http/connection_pool.py`
- Classe `ConnectionLimiter`
  - Méthodes : `__init__`

## `infrastructure/http/proxy.py`
- Fonctions : `normalize_proxy`

## `infrastructure/http/retry.py`
- Fonctions : `retry_async`

## `infrastructure/http/tls.py`
- Fonctions : `secure_ssl_context`

## `infrastructure/locking/process_lock.py`
- Classe `ProcessLock`
  - Méthodes : `__init__`, `acquire`, `release`

## `infrastructure/locking/resource_lock.py`
- Classe `ResourceLockRegistry`
  - Méthodes : `__init__`, `get`

## `infrastructure/queue/dead_letter_queue.py`
- Fonctions : `dead_letters`

## `infrastructure/queue/delayed_queue.py`
- Fonctions : `enqueue_delayed`

## `infrastructure/queue/durable_queue.py`
- Classe `DurableQueue`
  - Méthodes : `__init__`, `enqueue`, `claim`, `complete`, `fail`, `retry_dead`, `stats`

## `infrastructure/queue/idempotent_executor.py`
- Fonctions : `execute_once`

## `infrastructure/queue/lease_manager.py`
- Fonctions : `recover_expired_leases`

## `infrastructure/queue/priority_queue.py`
- Fonctions : `enqueue_urgent`

## `infrastructure/queue/task.py`
- Classe `QueueTask`

## `infrastructure/queue/task_claim.py`
- Fonctions : `claim_next`

## `infrastructure/queue/task_serializer.py`
- Fonctions : `serialize_task`

## `infrastructure/scheduler/cron_parser.py`
- Fonctions : `interval_from_expression`

## `infrastructure/scheduler/distributed_lock.py`
- Classe `DistributedLock`

## `infrastructure/scheduler/job_registry.py`
- Classe `ScheduledJob`
- Classe `JobRegistry`
  - Méthodes : `__init__`, `register`

## `infrastructure/scheduler/missed_job_recovery.py`
- Fonctions : `last_run`, `record_run`

## `infrastructure/scheduler/scheduler.py`
- Classe `AsyncScheduler`
  - Méthodes : `__init__`, `_runner`, `run`, `stop`

## `infrastructure/secrets/encrypted_file_provider.py`
- Classe `EncryptedFileSecretStore`
  - Méthodes : `__init__`, `_load`, `get`, `set`

## `infrastructure/secrets/env_provider.py`
- Classe `EnvSecretStore`
  - Méthodes : `get`, `set`

## `infrastructure/secrets/keyring_provider.py`
- Classe `KeyringSecretStore`
  - Méthodes : `__init__`, `get`, `set`

## `infrastructure/secrets/secret_store.py`
- Classe `SecretStore`
  - Méthodes : `get`, `set`

## `infrastructure/secrets/windows_dpapi_provider.py`
- Classe `WindowsDPAPISecretStore`
  - Méthodes : `__init__`, `get`, `set`

## `integrations/alibaba/capability_registry.py`
- Classe `AlibabaCapabilities`
  - Méthodes : `can`

## `integrations/alibaba/client.py`
- Classe `AlibabaClient`
  - Méthodes : `__init__`, `call`, `search_distribution_products`, `distribution_product`, `dropshipping_product`, `product`, `product_inventory`, `sku_inventory`, `calculate_product_freight`, `calculate_order_freight`, `create_buy_now_order`, `create_trade_assurance_order`, `pay_dropshipping_order`, `payment_result`, `order_funds`, `order`, `orders`, `tracking`, `consume_events`, `confirm_events`, `suppliers`, `supplier_items`

## `integrations/alibaba/error_mapper.py`
- Classe `AlibabaAPIError`
  - Méthodes : `__init__`
- Fonctions : `inspect_alibaba_response`

## `integrations/alibaba/gateway.py`
- Classe `AlibabaGateway`
  - Méthodes : `__init__`, `close`, `call`

## `integrations/alibaba/mappers/order_mapper.py`
- Fonctions : `map_order`

## `integrations/alibaba/mappers/payment_mapper.py`
- Fonctions : `map_payment`

## `integrations/alibaba/mappers/product_mapper.py`
- Fonctions : `_find`, `map_alibaba_product`

## `integrations/alibaba/mappers/shipping_mapper.py`
- Fonctions : `map_shipping_quote`

## `integrations/alibaba/mappers/supplier_mapper.py`
- Fonctions : `map_supplier`

## `integrations/alibaba/mappers/tracking_mapper.py`
- Fonctions : `map_tracking`

## `integrations/alibaba/methods/events/tmc_messages_confirm.py`
- Classe `TmcMessagesConfirm`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/events/tmc_messages_consume.py`
- Classe `TmcMessagesConsume`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/events/tmc_queue_status.py`
- Classe `TmcQueueStatus`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/events/tmc_topics_get.py`
- Classe `TmcTopicsGet`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/events/tmc_user_permit.py`
- Classe `TmcUserPermit`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/events/tmc_websocket_adapter.py`
- Classe `TmcWebsocketAdapter`
  - Méthodes : `endpoint`

## `integrations/alibaba/methods/logistics/fulfillment_channels.py`
- Classe `FulfillmentChannels`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/logistics/order_freight_calculator.py`
- Classe `OrderFreightCalculator`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/logistics/order_logistics_get.py`
- Classe `OrderLogisticsGet`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/logistics/product_freight_calculator.py`
- Classe `ProductFreightCalculator`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/logistics/shipping_channels.py`
- Classe `ShippingChannels`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/logistics/shipping_submit.py`
- Classe `ShippingSubmit`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/logistics/tracking_get.py`
- Classe `TrackingGet`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/orders/buy_now_order_create.py`
- Classe `BuyNowOrderCreate`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/orders/intention_order_save.py`
- Classe `IntentionOrderSave`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/orders/order_payment_result.py`
- Classe `OrderPaymentResult`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/orders/seller_order_get.py`
- Classe `SellerOrderGet`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/orders/seller_order_list.py`
- Classe `SellerOrderList`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/orders/trade_address_list.py`
- Classe `TradeAddressList`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/orders/trade_address_save.py`
- Classe `TradeAddressSave`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/orders/trade_address_schema.py`
- Classe `TradeAddressSchema`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/orders/trade_assurance_order_create.py`
- Classe `TradeAssuranceOrderCreate`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/payments/dropshipping_order_pay.py`
- Classe `DropshippingOrderPay`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/payments/order_funds_get.py`
- Classe `OrderFundsGet`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/payments/payment_capability_probe.py`
- Classe `PaymentCapabilityProbe`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/payments/payment_result_query.py`
- Classe `PaymentResultQuery`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/payments/service_charge_get.py`
- Classe `ServiceChargeGet`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/products/category_attributes_get.py`
- Classe `CategoryAttributesGet`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/products/category_get.py`
- Classe `CategoryGet`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/products/distribution_product_get.py`
- Classe `DistributionProductGet`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/products/distribution_product_query.py`
- Classe `DistributionProductQuery`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/products/dropshipping_product_get.py`
- Classe `DropshippingProductGet`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/products/dropshipping_token_create.py`
- Classe `DropshippingTokenCreate`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/products/inventory_get.py`
- Classe `InventoryGet`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/products/logistics_country_cost_status.py`
- Classe `LogisticsCountryCostStatus`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/products/photobank_list.py`
- Classe `PhotobankList`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/products/product_get.py`
- Classe `ProductGet`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/products/product_list.py`
- Classe `ProductList`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/products/product_schema_get.py`
- Classe `ProductSchemaGet`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/products/sku_inventory_get.py`
- Classe `SkuInventoryGet`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/suppliers/company_profile_get.py`
- Classe `CompanyProfileGet`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/suppliers/member_profile_get.py`
- Classe `MemberProfileGet`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/suppliers/supplier_credit_report.py`
- Classe `SupplierCreditReport`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/suppliers/supplier_items_get.py`
- Classe `SupplierItemsGet`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/methods/suppliers/supplier_list.py`
- Classe `SupplierList`
  - Méthodes : `__init__`, `execute`

## `integrations/alibaba/oauth.py`
- Classe `AlibabaOAuth`
  - Méthodes : `__init__`, `authorization_url`, `exchange_code`, `refresh`

## `integrations/alibaba/permission_probe.py`
- Classe `AlibabaPermissionProbe`
  - Méthodes : `__init__`, `probe_read_capabilities`

## `integrations/alibaba/rate_limit_manager.py`
- Classe `AlibabaRateLimitManager`
  - Méthodes : `__init__`, `wait`

## `integrations/alibaba/repositories/logistics_repository.py`
- Classe `LogisticsRepository`
  - Méthodes : `__init__`, `resource`

## `integrations/alibaba/repositories/order_repository.py`
- Classe `OrderRepository`
  - Méthodes : `__init__`, `resource`

## `integrations/alibaba/repositories/payment_repository.py`
- Classe `PaymentRepository`
  - Méthodes : `__init__`, `resource`

## `integrations/alibaba/repositories/product_repository.py`
- Classe `ProductRepository`
  - Méthodes : `__init__`, `resource`

## `integrations/alibaba/repositories/supplier_repository.py`
- Classe `SupplierRepository`
  - Méthodes : `__init__`, `resource`

## `integrations/alibaba/request_builder.py`
- Fonctions : `encode_business_parameters`

## `integrations/alibaba/response_parser.py`
- Fonctions : `first_response_node`

## `integrations/alibaba/retry_policy.py`
- Fonctions : `retry_delay`

## `integrations/alibaba/signer.py`
- Classe `AlibabaSigner`
  - Méthodes : `__init__`, `canonical`, `sign`, `signed_params`

## `integrations/alibaba/timestamp_service.py`
- Fonctions : `alibaba_timestamp`

## `integrations/alibaba/token_manager.py`
- Classe `AlibabaTokenManager`
  - Méthodes : `__init__`, `access_token`, `refresh_token`

## `integrations/currency/bank_of_canada_provider.py`
- Classe `BankOfCanadaRateProvider`
  - Méthodes : `rate`

## `integrations/currency/converter.py`
- Classe `CurrencyConverter`
  - Méthodes : `__init__`, `convert`

## `integrations/currency/rate_cache.py`
- Classe `ExchangeRateCache`

## `integrations/currency/shopify_market_provider.py`
- Classe `ShopifyMarketRateProvider`
  - Méthodes : `__init__`, `rate`

## `integrations/currency/static_rate_provider.py`
- Classe `StaticRateProvider`
  - Méthodes : `__init__`, `rate`

## `integrations/notifications/critical_alert_notifier.py`
- Classe `CriticalAlertNotifier`
  - Méthodes : `__init__`, `notify`

## `integrations/notifications/email_notifier.py`
- Classe `EmailNotifier`
  - Méthodes : `__init__`, `send`

## `integrations/notifications/notification_service.py`
- Classe `NotificationService`
  - Méthodes : `__init__`, `info`, `critical`

## `integrations/notifications/terminal_notifier.py`
- Classe `TerminalNotifier`
  - Méthodes : `__init__`, `info`, `warning`, `critical`

## `integrations/shopify/bulk_operations.py`
- Classe `ShopifyBulkOperations`
  - Méthodes : `__init__`, `export_products`

## `integrations/shopify/capability_registry.py`
- Classe `ShopifyCapabilities`
  - Méthodes : `can`

## `integrations/shopify/client.py`
- Classe `ShopifyClient`
  - Méthodes : `__init__`, `_user_errors`, `shop`, `current_app_installation`, `products`, `product_by_id`, `product_set`, `publish`, `publications`, `orders`, `order`, `inventory_set`, `fulfillment_orders`, `create_fulfillment`, `update_tracking`, `webhooks`, `create_webhook`, `bulk_query`

## `integrations/shopify/cost_calculator.py`
- Fonctions : `requested_query_cost`

## `integrations/shopify/error_mapper.py`
- Classe `ShopifyAPIError`
  - Méthodes : `__init__`
- Fonctions : `raise_for_graphql_errors`

## `integrations/shopify/graphql_transport.py`
- Classe `ShopifyGraphQLTransport`
  - Méthodes : `__init__`, `close`, `execute`

## `integrations/shopify/id_converter.py`
- Fonctions : `to_gid`, `gid_numeric_id`

## `integrations/shopify/mappers/customer_mapper.py`
- Fonctions : `map_customer`

## `integrations/shopify/mappers/fulfillment_mapper.py`
- Fonctions : `map_fulfillment`

## `integrations/shopify/mappers/inventory_mapper.py`
- Fonctions : `map_inventory_level`

## `integrations/shopify/mappers/order_mapper.py`
- Fonctions : `map_shopify_order`

## `integrations/shopify/mappers/product_mapper.py`
- Fonctions : `map_shopify_product`

## `integrations/shopify/mappers/refund_mapper.py`
- Fonctions : `map_refund`

## `integrations/shopify/mappers/variant_mapper.py`
- Fonctions : `map_variant`

## `integrations/shopify/oauth.py`
- Classe `ShopifyOAuth`
  - Méthodes : `__init__`, `authorization_url`, `exchange_code`

## `integrations/shopify/pagination.py`
- Fonctions : `paginate`

## `integrations/shopify/repositories/fulfillment_repository.py`
- Classe `FulfillmentRepository`
  - Méthodes : `__init__`, `resource`

## `integrations/shopify/repositories/inventory_repository.py`
- Classe `InventoryRepository`
  - Méthodes : `__init__`, `resource`

## `integrations/shopify/repositories/order_repository.py`
- Classe `OrderRepository`
  - Méthodes : `__init__`, `resource`

## `integrations/shopify/repositories/product_repository.py`
- Classe `ProductRepository`
  - Méthodes : `__init__`, `resource`

## `integrations/shopify/repositories/webhook_repository.py`
- Classe `WebhookRepository`
  - Méthodes : `__init__`, `resource`

## `integrations/shopify/rest_compatibility_client.py`
- Classe `ShopifyRestCompatibilityClient`
  - Méthodes : `__init__`, `get`

## `integrations/shopify/retry_policy.py`
- Fonctions : `retry_delay`

## `integrations/shopify/schema_introspection.py`
- Fonctions : `introspect_type`

## `integrations/shopify/scope_validator.py`
- Classe `ScopeValidator`
  - Méthodes : `__init__`, `validate`

## `integrations/shopify/throttle_manager.py`
- Classe `ShopifyThrottleManager`
  - Méthodes : `__init__`, `observe`

## `integrations/shopify/token_manager.py`
- Classe `ShopifyTokenManager`
  - Méthodes : `__init__`, `access_token`, `configured`

## `integrations/shopify/webhooks/compliance_handlers.py`
- Classe `ComplianceWebhookHandlers`
  - Méthodes : `__init__`, `customer_data_request`, `customer_redact`, `shop_redact`

## `integrations/shopify/webhooks/deduplicator.py`
- Classe `WebhookDeduplicator`
  - Méthodes : `__init__`, `register`

## `integrations/shopify/webhooks/dispatcher.py`
- Classe `ShopifyWebhookDispatcher`
  - Méthodes : `__init__`, `dispatch`

## `integrations/shopify/webhooks/handlers/app_uninstalled.py`
- Fonctions : `handle`

## `integrations/shopify/webhooks/handlers/customer_data_request.py`
- Fonctions : `handle`

## `integrations/shopify/webhooks/handlers/customer_redact.py`
- Fonctions : `handle`

## `integrations/shopify/webhooks/handlers/fulfillments_update.py`
- Fonctions : `handle`

## `integrations/shopify/webhooks/handlers/inventory_update.py`
- Fonctions : `handle`

## `integrations/shopify/webhooks/handlers/orders_cancelled.py`
- Fonctions : `handle`

## `integrations/shopify/webhooks/handlers/orders_create.py`
- Fonctions : `handle`

## `integrations/shopify/webhooks/handlers/orders_fulfilled.py`
- Fonctions : `handle`

## `integrations/shopify/webhooks/handlers/orders_paid.py`
- Fonctions : `handle`

## `integrations/shopify/webhooks/handlers/orders_updated.py`
- Fonctions : `handle`

## `integrations/shopify/webhooks/handlers/products_delete.py`
- Fonctions : `handle`

## `integrations/shopify/webhooks/handlers/products_update.py`
- Fonctions : `handle`

## `integrations/shopify/webhooks/handlers/refunds_create.py`
- Fonctions : `handle`

## `integrations/shopify/webhooks/handlers/returns_update.py`
- Fonctions : `handle`

## `integrations/shopify/webhooks/handlers/scopes_update.py`
- Fonctions : `handle`

## `integrations/shopify/webhooks/handlers/shop_redact.py`
- Fonctions : `handle`

## `integrations/shopify/webhooks/receiver.py`
- Fonctions : `build_shopify_webhook_router`

## `integrations/shopify/webhooks/subscription_manager.py`
- Classe `WebhookSubscriptionManager`
  - Méthodes : `__init__`, `ensure`

## `inventory/inventory_mirror.py`
- Classe `InventoryMirror`
  - Méthodes : `__init__`, `update_variant`

## `inventory/inventory_reconciler.py`
- Classe `InventoryReconciler`
  - Méthodes : `compare`

## `inventory/inventory_reservation.py`
- Classe `InventoryReservation`
  - Méthodes : `__init__`, `reserve`, `release`, `quantity`

## `inventory/out_of_stock_handler.py`
- Fonctions : `product_status_for_stock`

## `inventory/safety_stock.py`
- Fonctions : `available_for_sale`

## `inventory/sku_crosswalk.py`
- Classe `SKUCrosswalk`
  - Méthodes : `__init__`, `find`

## `inventory/stale_inventory_detector.py`
- Fonctions : `is_stale`

## `inventory/stock_update_scheduler.py`
- Fonctions : `schedule_stock_update`

## `main.py`
- Fonctions : `parser`, `async_main`, `cli`

## `migrations/env.py`
- Fonctions : `run_migrations`

## `observability/alert_manager.py`
- Classe `Alert`
- Classe `AlertManager`
  - Méthodes : `__init__`, `add`, `snapshot`

## `observability/api_metrics.py`
- Classe `ApiMetrics`
  - Méthodes : `record`

## `observability/business_metrics.py`
- Classe `BusinessMetrics`
  - Méthodes : `record`

## `observability/correlation.py`
- Fonctions : `ensure_correlation_id`

## `observability/counters.py`
- Classe `ThreadSafeCounters`
  - Méthodes : `__init__`, `increment`, `snapshot`

## `observability/incident_recorder.py`
- Fonctions : `record_incident`

## `observability/log_rotation.py`
- Fonctions : `force_log_flush`

## `observability/logger.py`
- Classe `JsonFormatter`
  - Méthodes : `format`
- Fonctions : `redact`, `configure_logging`, `get_logger`

## `observability/metrics.py`
- Classe `MetricsRegistry`
  - Méthodes : `inc`, `set`, `snapshot`

## `observability/resource_metrics.py`
- Classe `ResourceMetrics`
  - Méthodes : `record`

## `observability/structured_logging.py`
- Fonctions : `log_event`

## `observability/timers.py`
- Fonctions : `timer`

## `pricing/competitor_price_adapter.py`
- Fonctions : `choose_market_aware_price`

## `pricing/currency_adjuster.py`
- Fonctions : `convert`

## `pricing/gross_margin_calculator.py`
- Fonctions : `sale_price_for_margin`, `gross_margin_percent`

## `pricing/landed_cost_calculator.py`
- Classe `LandedCostBreakdown`
- Classe `LandedCostCalculator`
  - Méthodes : `calculate`

## `pricing/markup_calculator.py`
- Fonctions : `sale_price_for_markup`

## `pricing/platform_fee_estimator.py`
- Fonctions : `estimate_fee`

## `pricing/price_guardrails.py`
- Fonctions : `validate_price`

## `pricing/pricing_engine.py`
- Classe `PriceDecision`
- Classe `PricingEngine`
  - Méthodes : `__init__`, `calculate`

## `pricing/psychological_pricing.py`
- Fonctions : `psychological_price`

## `pricing/repricing_scheduler.py`
- Fonctions : `schedule_reprice`

## `pricing/shipping_cost_allocator.py`
- Fonctions : `allocate_shipping`

## `pricing/tax_estimator.py`
- Fonctions : `estimate_taxable_buffer`

## `procurement/address_builder.py`
- Fonctions : `build_supplier_address`

## `procurement/batch_builder.py`
- Classe `BatchBuilder`
  - Méthodes : `__init__`, `get_or_create_open_batch`, `add_order`, `ready_orders`

## `procurement/batch_optimizer.py`
- Fonctions : `optimize_order_sequence`

## `procurement/batch_reconciler.py`
- Classe `BatchReconciler`
  - Méthodes : `__init__`, `reconcile`

## `procurement/cancellation_handler.py`
- Fonctions : `cancel_pending_order`

## `procurement/order_line_aggregator.py`
- Fonctions : `aggregate`

## `procurement/partial_failure_handler.py`
- Fonctions : `partial_failure_result`

## `procurement/payment_approval_gate.py`
- Classe `PaymentApprovalGate`
  - Méthodes : `__init__`, `request`, `approved`, `decide`

## `procurement/payment_orchestrator.py`
- Classe `PaymentOrchestrator`
  - Méthodes : `__init__`, `pay`

## `procurement/payment_result_monitor.py`
- Classe `PaymentResultMonitor`
  - Méthodes : `__init__`, `check`

## `procurement/procurement_engine.py`
- Classe `ProcurementEngine`
  - Méthodes : `__init__`, `accumulate_paid_orders`, `evaluate_batch`, `submit_batch`

## `procurement/purchase_order_builder.py`
- Classe `PurchaseOrderBuilder`
  - Méthodes : `build`

## `procurement/supplier_splitter.py`
- Fonctions : `split_by_supplier`

## `procurement/threshold_manager.py`
- Classe `ThresholdDecision`
- Classe `ThresholdManager`
  - Méthodes : `__init__`, `evaluate`

## `reports/ai_performance_report.py`
- Classe `AIPerformanceReport`
  - Méthodes : `__init__`, `generate`

## `reports/audit_report.py`
- Classe `AuditReport`
  - Méthodes : `__init__`, `generate`

## `reports/csv_exporter.py`
- Fonctions : `export_csv`

## `reports/daily_report.py`
- Classe `DailyReport`
  - Méthodes : `__init__`, `generate`

## `reports/inventory_report.py`
- Classe `InventoryReport`
  - Méthodes : `__init__`, `generate`

## `reports/json_exporter.py`
- Fonctions : `export_json`

## `reports/monthly_report.py`
- Classe `MonthlyReport`
  - Méthodes : `__init__`, `generate`

## `reports/profit_report.py`
- Classe `ProfitReport`
  - Méthodes : `__init__`, `generate`

## `reports/refund_report.py`
- Classe `RefundReport`
  - Méthodes : `__init__`, `generate`

## `reports/shipping_report.py`
- Classe `ShippingReport`
  - Méthodes : `__init__`, `generate`

## `reports/supplier_report.py`
- Classe `SupplierReport`
  - Méthodes : `__init__`, `generate`

## `reports/weekly_report.py`
- Classe `WeeklyReport`
  - Méthodes : `__init__`, `generate`

## `scripts/initialize_project.py`
- Fonctions : `run`

## `scripts/reconcile_all.py`
- Fonctions : `run`

## `scripts/register_shopify_webhooks.py`
- Fonctions : `run`

## `security/access_control.py`
- Fonctions : `verify_admin_token`

## `security/audit_logger.py`
- Classe `AuditLogger`
  - Méthodes : `__init__`, `record`

## `security/data_retention.py`
- Fonctions : `retention_cutoff`

## `security/encryption.py`
- Classe `EncryptionService`
  - Méthodes : `__init__`, `encrypt`, `decrypt`
- Fonctions : `derive_fernet_key`

## `security/field_encryption.py`
- Classe `FieldEncryption`
  - Méthodes : `__init__`, `encrypt_mapping`, `decrypt_mapping`

## `security/pci_guard.py`
- Fonctions : `reject_payment_card_data`

## `security/pii_vault.py`
- Classe `PIIVault`
  - Méthodes : `__init__`, `store_address`, `read_address`

## `security/replay_protection.py`
- Fonctions : `timestamp_within_window`

## `security/request_signing.py`
- Fonctions : `hmac_sha256_hex`

## `security/secret_scanner.py`
- Fonctions : `_luhn_valid`, `scan_text`, `scan_tree`

## `security/secure_delete.py`
- Fonctions : `secure_delete`

## `security/token_redactor.py`
- Fonctions : `redact_text`

## `security/webhook_security.py`
- Fonctions : `verify_shopify_hmac`

## `tests/conftest.py`
- Fonctions : `settings`, `db`

## `tests/contract/test_alibaba_method_contract.py`
- Fonctions : `test_required_methods`

## `tests/contract/test_currency_contract.py`
- Fonctions : `test_currency`

## `tests/contract/test_shopify_schema_contract.py`
- Fonctions : `test_contract_fields`

## `tests/contract/test_webhook_payload_contract.py`
- Fonctions : `test_order_webhook_minimum`

## `tests/end_to_end/test_paid_order_to_alibaba.py`
- Fonctions : `test_procurement_engine_import`

## `tests/end_to_end/test_product_to_shopify.py`
- Fonctions : `test_product_pipeline_modules_import`

## `tests/end_to_end/test_recovery_after_crash.py`
- Fonctions : `test_task_survives_new_queue_instance`

## `tests/end_to_end/test_refund_flow.py`
- Fonctions : `test_refund_reserve`

## `tests/end_to_end/test_tracking_to_shopify.py`
- Fonctions : `test_tracking_sync_import`

## `tests/integration/test_alibaba_gateway.py`
- Fonctions : `test_alibaba_common_signing`

## `tests/integration/test_alibaba_orders.py`
- Fonctions : `test_order_mapping`

## `tests/integration/test_alibaba_products.py`
- Fonctions : `test_product_mapping`

## `tests/integration/test_alibaba_shipping.py`
- Fonctions : `test_shipping_mapping`

## `tests/integration/test_database.py`
- Fonctions : `test_database_health`

## `tests/integration/test_runtime.py`
- Fonctions : `test_container`

## `tests/integration/test_shopify_graphql.py`
- Fonctions : `test_shopify_url`

## `tests/integration/test_shopify_inventory.py`
- Fonctions : `test_inventory_reconcile`

## `tests/integration/test_shopify_webhooks.py`
- Fonctions : `test_dedup`

## `tests/performance/test_750mb_limit.py`
- Fonctions : `test_memory_limit`

## `tests/performance/test_api_backpressure.py`
- Fonctions : `test_http_concurrency`

## `tests/performance/test_dashboard_refresh.py`
- Fonctions : `test_dashboard_default`

## `tests/performance/test_dual_core_runtime.py`
- Fonctions : `test_threads_limited`

## `tests/performance/test_queue_throughput.py`
- Fonctions : `test_small_queue_batch`

## `tests/security/test_payment_data_guard.py`
- Fonctions : `test_card_data_rejected`

## `tests/security/test_pii_encryption.py`
- Fonctions : `test_encryption_roundtrip`

## `tests/security/test_replay_protection.py`
- Fonctions : `test_current_timestamp`

## `tests/security/test_secret_redaction.py`
- Fonctions : `test_redaction`

## `tests/security/test_webhook_spoofing.py`
- Fonctions : `test_fake_signature_rejected`

## `tests/unit/test_ai_memory_budget.py`
- Fonctions : `test_memory_budget_snapshot`

## `tests/unit/test_batch_builder.py`
- Fonctions : `test_batch_creation`

## `tests/unit/test_compliance_filters.py`
- Fonctions : `test_restricted`

## `tests/unit/test_idempotency.py`
- Fonctions : `test_key_stable`

## `tests/unit/test_inventory_sync.py`
- Fonctions : `test_safety_stock`

## `tests/unit/test_landed_cost.py`
- Fonctions : `test_landed_cost_contains_buffers`

## `tests/unit/test_money.py`
- Fonctions : `test_money_arithmetic`

## `tests/unit/test_pricing_engine.py`
- Fonctions : `test_real_fifty_percent_margin`

## `tests/unit/test_queue.py`
- Fonctions : `test_queue_claim_complete`

## `tests/unit/test_signature.py`
- Fonctions : `test_sign_is_deterministic`

## `tests/unit/test_state_machines.py`
- Fonctions : `test_payment_transition`

## `tests/unit/test_webhook_hmac.py`
- Fonctions : `test_shopify_hmac`

## `tools/alibaba_connection_test.py`
- Fonctions : `run`

## `tools/alibaba_method_tester.py`
- Fonctions : `run`

## `tools/alibaba_permission_probe.py`
- Fonctions : `run`

## `tools/alibaba_signature_tester.py`
- Fonctions : `test_vector`

## `tools/database_inspector.py`
- Fonctions : `run`

## `tools/emergency_recovery.py`
- Fonctions : `run`

## `tools/load_test.py`
- Fonctions : `run`

## `tools/memory_profiler.py`
- Fonctions : `run`

## `tools/model_benchmark.py`
- Fonctions : `run`

## `tools/payment_capability_tester.py`
- Fonctions : `run`

## `tools/queue_inspector.py`
- Fonctions : `run`

## `tools/shipping_quote_tester.py`
- Fonctions : `run`

## `tools/shopify_connection_test.py`
- Fonctions : `run`

## `tools/shopify_schema_probe.py`
- Fonctions : `run`

## `tools/shopify_scope_inspector.py`
- Fonctions : `run`

## `tools/shopify_webhook_tester.py`
- Fonctions : `signed_headers`

## `workers/accounting_worker.py`
- Classe `AccountingWorker`
  - Méthodes : `__init__`, `run`

## `workers/ai_training_worker.py`
- Classe `AiTrainingWorker`
  - Méthodes : `__init__`, `run`

## `workers/alibaba_event_worker.py`
- Classe `AlibabaEventWorker`
  - Méthodes : `__init__`, `run`

## `workers/catalog_sync_worker.py`
- Classe `CatalogSyncWorker`
  - Méthodes : `__init__`, `run`

## `workers/cleanup_worker.py`
- Classe `CleanupWorker`
  - Méthodes : `__init__`, `run`

## `workers/dead_letter_worker.py`
- Classe `DeadLetterWorker`
  - Méthodes : `__init__`, `run_once`

## `workers/fulfillment_worker.py`
- Classe `FulfillmentWorker`
  - Méthodes : `__init__`, `run`

## `workers/heartbeat.py`
- Classe `Heartbeat`
  - Méthodes : `__init__`, `beat`

## `workers/inventory_sync_worker.py`
- Classe `InventorySyncWorker`
  - Méthodes : `__init__`, `run`

## `workers/order_worker.py`
- Classe `OrderWorker`
  - Méthodes : `__init__`, `run`

## `workers/payment_worker.py`
- Classe `PaymentWorker`
  - Méthodes : `__init__`, `run`

## `workers/pricing_worker.py`
- Classe `PricingWorker`
  - Méthodes : `__init__`, `run`

## `workers/procurement_worker.py`
- Classe `ProcurementWorker`
  - Méthodes : `__init__`, `run`

## `workers/product_discovery_worker.py`
- Classe `ProductDiscoveryWorker`
  - Méthodes : `__init__`, `run`

## `workers/reconciliation_worker.py`
- Classe `ReconciliationWorker`
  - Méthodes : `__init__`, `run`

## `workers/resource_monitor.py`
- Classe `ResourceMonitor`
  - Méthodes : `snapshot`

## `workers/retry_worker.py`
- Classe `RetryWorker`
  - Méthodes : `__init__`, `retry`

## `workers/shopify_event_worker.py`
- Classe `ShopifyEventWorker`
  - Méthodes : `__init__`, `run`

## `workers/supervisor.py`
- Classe `WorkerSupervisor`
  - Méthodes : `__init__`, `run`, `stop`

## `workers/tracking_worker.py`
- Classe `TrackingWorker`
  - Méthodes : `__init__`, `run`

## `workers/watchdog.py`
- Classe `Watchdog`
  - Méthodes : `__init__`, `recover`

## `workers/worker_context.py`
- Classe `WorkerContext`

## `workflows/alibaba_order_workflow.py`
- Classe `AlibabaOrderWorkflow`
  - Méthodes : `__init__`, `execute`

## `workflows/alibaba_payment_workflow.py`
- Classe `AlibabaPaymentWorkflow`
  - Méthodes : `__init__`, `execute`

## `workflows/alibaba_reconciliation_workflow.py`
- Classe `AlibabaReconciliationWorkflow`
  - Méthodes : `__init__`, `execute`

## `workflows/cancellation_workflow.py`
- Classe `CancellationWorkflow`
  - Méthodes : `__init__`, `execute`

## `workflows/daily_maintenance_workflow.py`
- Classe `DailyMaintenanceWorkflow`
  - Méthodes : `__init__`, `execute`

## `workflows/financial_reconciliation_workflow.py`
- Classe `FinancialReconciliationWorkflow`
  - Méthodes : `__init__`, `execute`

## `workflows/fulfillment_workflow.py`
- Classe `FulfillmentWorkflow`
  - Méthodes : `__init__`, `execute`

## `workflows/inventory_sync_workflow.py`
- Classe `InventorySyncWorkflow`
  - Méthodes : `__init__`, `execute`

## `workflows/order_intake_workflow.py`
- Classe `OrderIntakeWorkflow`
  - Méthodes : `__init__`, `execute`

## `workflows/payment_verification_workflow.py`
- Classe `PaymentVerificationWorkflow`
  - Méthodes : `verify`

## `workflows/pricing_update_workflow.py`
- Classe `PricingUpdateWorkflow`
  - Méthodes : `__init__`, `execute`

## `workflows/procurement_batch_workflow.py`
- Classe `ProcurementBatchWorkflow`
  - Méthodes : `__init__`, `execute`

## `workflows/product_discovery_workflow.py`
- Classe `ProductDiscoveryWorkflow`
  - Méthodes : `__init__`, `execute`

## `workflows/product_import_workflow.py`
- Classe `ProductImportWorkflow`
  - Méthodes : `__init__`, `execute`

## `workflows/product_unpublish_workflow.py`
- Classe `ProductUnpublishWorkflow`
  - Méthodes : `__init__`, `execute`

## `workflows/product_update_workflow.py`
- Classe `ProductUpdateWorkflow`
  - Méthodes : `__init__`, `execute`

## `workflows/refund_workflow.py`
- Classe `RefundWorkflow`
  - Méthodes : `__init__`, `execute`

## `workflows/return_workflow.py`
- Classe `ReturnWorkflow`
  - Méthodes : `__init__`, `execute`

## `workflows/shipping_quote_workflow.py`
- Classe `ShippingQuoteWorkflow`
  - Méthodes : `__init__`, `execute`

## `workflows/shopify_reconciliation_workflow.py`
- Classe `ShopifyReconciliationWorkflow`
  - Méthodes : `__init__`, `execute`

## `workflows/tracking_sync_workflow.py`
- Classe `TrackingSyncWorkflow`
  - Méthodes : `__init__`, `execute`
