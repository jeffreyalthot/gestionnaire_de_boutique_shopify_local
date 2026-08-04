from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any

from finance.daily_close import daily_close


class OperationHandlers:
    """Exécute les opérations planifiées sans autoriser de mutation implicite."""

    def __init__(self, container: Any) -> None:
        self.container = container

    async def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        operation = str(payload.get("operation", ""))
        cycle_id = str(payload.get("cycle_id", ""))
        dry_run = bool(payload.get("dry_run", self.container.settings.app_dry_run))
        method = getattr(self, f"op_{operation}", None)
        if method is None:
            result = self._inspect(operation)
        else:
            result = method(dry_run=dry_run)
            if asyncio.iscoroutine(result):
                result = await result
        detail = {
            "operation": operation,
            "cycle_id": cycle_id,
            "dry_run": dry_run,
            "result": result,
            "at": datetime.now(timezone.utc).isoformat(),
        }
        self.container.db.insert_audit("automation.operation", "automation-worker", detail)
        self.container.automation_state.record("completed", operation)
        return detail

    def _inspect(self, operation: str) -> dict[str, Any]:
        return {"status": "inspected", "operation": operation, "counts": self.container.db.counts()}

    def op_database_maintenance(self, *, dry_run: bool) -> dict[str, Any]:
        if dry_run:
            return {"status": "simulated", "integrity": self.container.db.health()}
        with self.container.db.connect() as conn:
            conn.execute("PRAGMA optimize")
            conn.execute("PRAGMA wal_checkpoint(PASSIVE)")
        return {"status": "completed", "integrity": self.container.db.health()}

    def op_financial_reconciliation(self, *, dry_run: bool) -> dict[str, Any]:
        if dry_run:
            return {"status": "simulated", "snapshot": self.container.db.financial_snapshot()}
        return {"status": "completed", "close": daily_close(self.container.db)}

    def op_paid_order_intake(self, *, dry_run: bool) -> dict[str, Any]:
        rows = self.container.db.query(
            "SELECT id,name,total_amount,procurement_status FROM orders "
            "WHERE financial_status IN ('paid','partially_paid') ORDER BY created_at LIMIT 100"
        )
        return {"status": "simulated" if dry_run else "reviewed", "orders": len(rows)}

    def op_supplier_order_planning(self, *, dry_run: bool) -> dict[str, Any]:
        batch = self.container.procurement.accumulate_paid_orders()
        return {"status": "simulated" if dry_run else "planned", "batch": batch,
                "decision": self.container.procurement.evaluate_batch(batch)}

    def op_customer_ticket_triage(self, *, dry_run: bool) -> dict[str, Any]:
        rows = self.container.db.query(
            "SELECT category,COUNT(*) count FROM customer_tickets WHERE status='open' GROUP BY category"
        )
        return {"status": "simulated" if dry_run else "triaged", "categories": rows}


    async def op_catalog_discovery(self, *, dry_run: bool) -> dict[str, Any]:
        if dry_run:
            row = self.container.db.query_one("SELECT COUNT(*) count FROM products WHERE status IN ('candidate','draft')") or {"count": 0}
            return {"status": "simulated", "existing_candidates": int(row["count"])}
        from catalog.catalog_automation_service import CatalogAutomationService
        from catalog.discovery.search_plan import SearchPlan
        queries = tuple(item.strip() for item in self.container.settings.product_discovery_keywords.split(",") if item.strip())
        plan = SearchPlan(
            queries=queries,
            page_size=self.container.settings.product_discovery_page_size,
            max_pages=self.container.settings.product_discovery_max_pages,
            max_candidates=self.container.settings.product_discovery_max_candidates,
        )
        return await CatalogAutomationService(self.container).discover(plan)

    def op_media_import(self, *, dry_run: bool) -> dict[str, Any]:
        rows = self.container.db.query("SELECT status,COUNT(*) count FROM media_assets GROUP BY status")
        return {"status": "simulated" if dry_run else "reviewed", "assets": rows, "rights_gate": "required"}

    def op_catalog_publication_review(self, *, dry_run: bool) -> dict[str, Any]:
        row = self.container.db.query_one(
            "SELECT COUNT(*) total, SUM(CASE WHEN score>=? AND status='draft' THEN 1 ELSE 0 END) eligible FROM products",
            (self.container.settings.product_minimum_score,),
        ) or {"total": 0, "eligible": 0}
        return {"status": "simulated" if dry_run else "reviewed", **row, "approval_required": True}

    def op_catalog_quality_review(self, *, dry_run: bool) -> dict[str, Any]:
        row = self.container.db.query_one(
            "SELECT COUNT(*) total, SUM(CASE WHEN score>=0.7 THEN 1 ELSE 0 END) eligible FROM products"
        ) or {"total": 0, "eligible": 0}
        return {"status": "simulated" if dry_run else "reviewed", **row}

    def op_inventory_reconciliation(self, *, dry_run: bool) -> dict[str, Any]:
        row = self.container.db.query_one(
            "SELECT COUNT(*) products, SUM(CASE WHEN stock<=? THEN 1 ELSE 0 END) low_stock FROM products",
            (self.container.settings.inventory_low_stock_threshold,),
        ) or {"products": 0, "low_stock": 0}
        return {"status": "simulated" if dry_run else "reviewed", **row}

    def op_price_recalculation(self, *, dry_run: bool) -> dict[str, Any]:
        row = self.container.db.query_one(
            "SELECT COUNT(*) products, AVG(sale_price_cad) average_price FROM products"
        ) or {"products": 0, "average_price": 0}
        return {"status": "simulated" if dry_run else "reviewed", **row}

    def op_tracking_reconciliation(self, *, dry_run: bool) -> dict[str, Any]:
        row = self.container.db.query_one(
            "SELECT COUNT(*) shipments, SUM(CASE WHEN tracking_number='' THEN 1 ELSE 0 END) missing_tracking FROM shipments"
        ) or {"shipments": 0, "missing_tracking": 0}
        return {"status": "simulated" if dry_run else "reviewed", **row}

    def op_order_risk_review(self, *, dry_run: bool) -> dict[str, Any]:
        rows = self.container.db.query(
            "SELECT risk_level,COUNT(*) count FROM orders GROUP BY risk_level"
        )
        return {"status": "simulated" if dry_run else "reviewed", "risk": rows}

    def op_compliance_rescan(self, *, dry_run: bool) -> dict[str, Any]:
        row = self.container.db.query_one(
            "SELECT COUNT(*) total, SUM(CASE WHEN status='quarantined' THEN 1 ELSE 0 END) quarantined FROM products"
        ) or {"total": 0, "quarantined": 0}
        return {"status": "simulated" if dry_run else "reviewed", **row}

    async def op_runtime_health_snapshot(self, *, dry_run: bool) -> dict[str, Any]:
        coordinator = self.container.runtime_coordinator
        if coordinator is None:
            return {"status": "unavailable"}
        snapshot = await coordinator.snapshot(persist=not dry_run)
        return {"status": "simulated" if dry_run else "persisted", "snapshot": snapshot.as_dict()}

    def op_exception_recovery(self, *, dry_run: bool) -> dict[str, Any]:
        from automation.exceptions.stuck_operation_detector import StuckOperationDetector

        ready = self.container.exception_queue.claim_ready(50)
        stuck = StuckOperationDetector(self.container.db).detect(50)
        recovery = {"recovered_leases": 0, "resumed_checkpoints": 0, "dead_tasks": 0}
        if not dry_run:
            recovery = self.container.recovery.recover().as_dict()
        return {
            "status": "simulated" if dry_run else "completed",
            "ready_exceptions": len(ready),
            "stuck_tasks": len(stuck),
            "recovery": recovery,
        }

    def op_analytics_snapshot(self, *, dry_run: bool) -> dict[str, Any]:
        from analytics.event_facts import EventFact
        from analytics.kpi_registry import default_registry

        counts = self.container.db.counts()
        finance = self.container.db.financial_snapshot()
        facts = {
            "orders": counts["orders"],
            "sessions": int(self.container.db.get_value("analytics:sessions", 0)),
            "revenue": finance["revenue"],
            "cogs": finance["supplier_cost"] + finance["shipping"],
            "refunds": int(self.container.db.scalar("SELECT COUNT(*) FROM payments WHERE status='refunded'", default=0)),
        }
        kpis = default_registry().calculate(facts)
        if not dry_run:
            self.container.analytics.record_many(
                EventFact(metric=name, value=value, dimensions={"store": self.container.settings.app_name})
                for name, value in kpis.items()
            )
        return {"status": "simulated" if dry_run else "persisted", "facts": facts, "kpis": kpis}

    def op_catalog_lifecycle_review(self, *, dry_run: bool) -> dict[str, Any]:
        from collections import Counter
        from catalog.lifecycle.product_lifecycle import ProductLifecycle

        products = self.container.db.query(
            "SELECT id,status,stock,score,updated_at FROM products ORDER BY updated_at LIMIT 500"
        )
        decisions = [ProductLifecycle().decide(product) for product in products]
        actions = Counter(item.action for item in decisions)
        return {
            "status": "simulated" if dry_run else "reviewed",
            "products": len(products),
            "actions": dict(actions),
            "mutations_applied": 0,
        }

    def op_supplier_score_refresh(self, *, dry_run: bool) -> dict[str, Any]:
        import json
        from suppliers.supplier_score import SupplierScorer
        from infrastructure.database.engine import utcnow

        suppliers = self.container.db.query("SELECT supplier_id,metrics_json FROM supplier_scores ORDER BY supplier_id LIMIT 500")
        scorer = SupplierScorer()
        updates = []
        for row in suppliers:
            metrics = json.loads(row["metrics_json"] or "{}")
            score = scorer.score(str(row["supplier_id"]), metrics)
            updates.append(score.as_dict())
            if not dry_run:
                self.container.db.execute(
                    "UPDATE supplier_scores SET score=?,risk_level=?,metrics_json=?,updated_at=? WHERE supplier_id=?",
                    (score.score, score.risk_level, json.dumps(score.metrics, ensure_ascii=False), utcnow(), score.supplier_id),
                )
        return {"status": "simulated" if dry_run else "updated", "suppliers": len(updates), "scores": updates[:20]}

    def op_customer_profile_refresh(self, *, dry_run: bool) -> dict[str, Any]:
        from customers.customer_lifetime_value import CustomerLifetimeValue
        from customers.customer_profile import CustomerProfile
        from customers.customer_tag_service import CustomerTagService
        from customers.customer_risk_profile import CustomerRiskProfiler

        rows = self.container.db.query(
            "SELECT customer_id,COUNT(*) order_count,COALESCE(SUM(profit_cad),0) profit,"
            "SUM(CASE WHEN financial_status IN ('refunded','partially_refunded') THEN 1 ELSE 0 END) refunds "
            "FROM orders WHERE customer_id<>'' GROUP BY customer_id LIMIT 500"
        )
        updated = 0
        for row in rows:
            customer_id = str(row["customer_id"])
            existing = self.container.customers.get(customer_id)
            order_count = int(row["order_count"])
            lifetime = max(0.0, float(row["profit"]))
            risk = CustomerRiskProfiler().evaluate(refunds=int(row["refunds"] or 0), orders=order_count)
            tags = CustomerTagService().build(
                lifetime_value_cad=lifetime,
                order_count=order_count,
                risk_score=risk.score,
                consented_marketing=self.container.consents.current(customer_id, "marketing"),
            )
            profile = CustomerProfile(
                customer_id=customer_id,
                email_hash=existing.email_hash if existing else "",
                country_code=existing.country_code if existing else "",
                language=existing.language if existing else "",
                lifetime_value_cad=lifetime,
                risk_score=risk.score,
                preferences=existing.preferences if existing else {},
                tags=tags,
                created_at=existing.created_at if existing else CustomerProfile(customer_id).created_at,
            )
            if not dry_run:
                self.container.customers.save(profile)
                self.container.segments.build(
                    customer_id,
                    lifetime_value_cad=lifetime,
                    order_count=order_count,
                    risk_score=risk.score,
                    days_since_last_order=0,
                )
            updated += 1
        return {"status": "simulated" if dry_run else "updated", "profiles": updated}

    def op_privacy_retention_review(self, *, dry_run: bool) -> dict[str, Any]:
        from datetime import datetime, timedelta, timezone

        address_cutoff = (datetime.now(timezone.utc) - timedelta(days=self.container.settings.customer_address_retention_days)).isoformat()
        addresses = int(self.container.db.scalar(
            "SELECT COUNT(*) FROM orders WHERE encrypted_shipping_address<>'' AND created_at<?",
            (address_cutoff,), default=0,
        ))
        stale_events = int(self.container.db.scalar(
            "SELECT COUNT(*) FROM events WHERE created_at<?",
            ((datetime.now(timezone.utc) - timedelta(days=30)).isoformat(),), default=0,
        ))
        return {
            "status": "simulated" if dry_run else "reviewed",
            "expired_addresses": addresses,
            "stale_webhook_events": stale_events,
            "automatic_deletion": False,
            "reason": "destructive_retention_requires_explicit_job",
        }

    def op_marketing_budget_review(self, *, dry_run: bool) -> dict[str, Any]:
        from finance.cash_reserve_policy import CashReservePolicy
        from finance.marketing_budget import MarketingBudget

        finance = self.container.db.financial_snapshot()
        available_cash = float(self.container.db.get_value("finance:available_cash_cad", 0.0))
        reserve = CashReservePolicy().calculate(
            trailing_refunds_cad=float(self.container.db.get_value("finance:trailing_refunds_cad", 0.0)),
            trailing_chargebacks_cad=float(self.container.db.get_value("finance:trailing_chargebacks_cad", 0.0)),
            pending_supplier_payments_cad=float(self.container.db.get_value("finance:pending_supplier_payments_cad", 0.0)),
            fixed_operating_cost_cad=float(self.container.db.get_value("finance:fixed_operating_cost_cad", 0.0)),
        )
        budget = MarketingBudget().allocate(
            available_cash_cad=available_cash,
            reserve_required_cad=float(reserve["required_reserve_cad"]),
            trailing_profit_cad=finance["profit"],
        )
        return {"status": "simulated" if dry_run else "reviewed", "reserve": reserve, "budget": budget}

    def op_financial_reserve_review(self, *, dry_run: bool) -> dict[str, Any]:
        from finance.cash_reserve_policy import CashReservePolicy
        from finance.chargeback_reserve import chargeback_reserve
        from finance.duty_reserve import duty_reserve
        from finance.tax_reserve import tax_reserve

        revenue = self.container.db.financial_snapshot()["revenue"]
        chargebacks = chargeback_reserve(
            revenue,
            float(self.container.db.get_value("finance:chargeback_rate", 0.01)),
        )
        duties = duty_reserve(
            float(self.container.db.get_value("finance:pending_import_value_cad", 0.0)),
            float(self.container.db.get_value("finance:estimated_duty_rate", 0.0)),
        )
        taxes = tax_reserve(
            float(self.container.db.get_value("finance:tax_collected_cad", 0.0)),
            float(self.container.db.get_value("finance:tax_refunded_cad", 0.0)),
        )
        cash = CashReservePolicy().calculate(
            trailing_refunds_cad=float(self.container.db.get_value("finance:trailing_refunds_cad", 0.0)),
            trailing_chargebacks_cad=chargebacks,
            pending_supplier_payments_cad=float(self.container.db.get_value("finance:pending_supplier_payments_cad", 0.0)),
            fixed_operating_cost_cad=float(self.container.db.get_value("finance:fixed_operating_cost_cad", 0.0)),
        )
        return {
            "status": "simulated" if dry_run else "reviewed",
            "cash_reserve": cash,
            "chargeback_reserve_cad": chargebacks,
            "duty_reserve_cad": duties,
            "tax_reserve_cad": taxes,
            "total_protected_cad": round(float(cash["required_reserve_cad"]) + duties + taxes, 2),
        }

    def op_inventory_reservation_audit(self, *, dry_run: bool) -> dict[str, Any]:
        summary = self.container.db.query_one(
            "SELECT COUNT(*) positions,COALESCE(SUM(on_hand),0) on_hand,"
            "COALESCE(SUM(reserved),0) reserved,"
            "COALESCE(SUM(CASE WHEN reserved>on_hand THEN 1 ELSE 0 END),0) oversubscribed,"
            "COALESCE(SUM(CASE WHEN on_hand-reserved<=safety_stock THEN 1 ELSE 0 END),0) low_stock "
            "FROM inventory_positions"
        ) or {}
        return {"status": "simulated" if dry_run else "audited", **summary}

    def op_purchase_intent_recovery(self, *, dry_run: bool) -> dict[str, Any]:
        rows = self.container.db.query(
            "SELECT id,status,updated_at,error FROM purchase_intents "
            "WHERE status IN ('creating','paying','retry','failed') ORDER BY updated_at LIMIT 100"
        )
        repaired = 0
        if not dry_run:
            for row in rows:
                if row["status"] in {"creating", "paying"}:
                    repaired += self.container.db.execute(
                        "UPDATE purchase_intents SET status='retry',updated_at=? WHERE id=? AND status=?",
                        (datetime.now(timezone.utc).isoformat(), row["id"], row["status"]),
                    )
        return {"status": "simulated" if dry_run else "recovered", "candidates": len(rows), "repaired": repaired}

    def op_fraud_posture_snapshot(self, *, dry_run: bool) -> dict[str, Any]:
        rows = self.container.db.query(
            "SELECT risk_level,COUNT(*) count,COALESCE(SUM(total_amount),0) exposure_cad "
            "FROM orders GROUP BY risk_level"
        )
        held = int(self.container.db.scalar("SELECT COUNT(*) FROM risk_decisions WHERE held=1", default=0))
        return {"status": "simulated" if dry_run else "reviewed", "risk_buckets": rows, "persisted_holds": held}

    def op_campaign_schedule_review(self, *, dry_run: bool) -> dict[str, Any]:
        from marketing.campaign_scheduler import CampaignScheduler

        campaigns = self.container.campaigns.list()
        due = CampaignScheduler().due(campaigns)
        return {
            "status": "simulated" if dry_run else "reviewed",
            "campaigns": len(campaigns),
            "due": len(due),
            "automatic_launch": False,
        }

    def op_store_configuration_audit(self, *, dry_run: bool) -> dict[str, Any]:
        from store_management.domain_auditor import DomainAuditor
        from store_management.shop_policy_manager import ShopPolicyManager

        domain = self.container.settings.shopify_shop_domain
        canonical = domain
        domain_report = DomainAuditor().audit(domain or "https://unconfigured.invalid", canonical or "unconfigured.invalid")
        policies = self.container.db.get_value("store:policies", {})
        policy_report = ShopPolicyManager().completeness(policies if isinstance(policies, dict) else {})
        return {"status": "simulated" if dry_run else "audited", "domain": domain_report, "policies": policy_report}

    def op_sales_channel_review(self, *, dry_run: bool) -> dict[str, Any]:
        return {
            "status": "simulated" if dry_run else "reviewed",
            "registered_channels": self.container.sales_channels.names(),
            "publication_mutations": 0,
        }

    def op_security_integrity_review(self, *, dry_run: bool) -> dict[str, Any]:
        audit = self.container.db.verify_audit_chain()
        lockdown = self.container.lockdown.snapshot()
        with self.container.db.connect() as conn:
            integrity = str(conn.execute("PRAGMA quick_check").fetchone()[0])
        return {
            "status": "simulated" if dry_run else "reviewed",
            "audit_chain": audit,
            "sqlite_quick_check": integrity,
            "lockdown": lockdown,
            "ok": bool(audit.get("ok") and integrity == "ok" and not lockdown["active"]),
        }

    def op_oauth_state_cleanup(self, *, dry_run: bool) -> dict[str, Any]:
        now = datetime.now(timezone.utc).isoformat()
        count = int(self.container.db.scalar(
            "SELECT COUNT(*) FROM oauth_states WHERE expires_at<? OR consumed_at IS NOT NULL", (now,), default=0
        ))
        deleted = 0 if dry_run else self.container.db.execute(
            "DELETE FROM oauth_states WHERE expires_at<? OR consumed_at IS NOT NULL", (now,)
        )
        return {"status": "simulated" if dry_run else "cleaned", "eligible": count, "deleted": deleted}


    def op_dead_letter_review(self, *, dry_run: bool) -> dict[str, Any]:
        rows = self.container.db.query("SELECT queue,task_type,COUNT(*) count FROM tasks WHERE status='dead' GROUP BY queue,task_type ORDER BY count DESC LIMIT 100")
        return {"status": "simulated" if dry_run else "reviewed", "groups": rows, "dead": sum(int(row["count"]) for row in rows)}

    def op_channel_feed_review(self, *, dry_run: bool) -> dict[str, Any]:
        products = self.container.db.query("SELECT id,title,description,sale_price_cad price_cad,stock,data_json FROM products WHERE status IN ('active','published','draft') ORDER BY score DESC LIMIT 100")
        reviewed = {}
        for channel in self.container.sales_channels.names():
            adapter = self.container.sales_channels.get(channel)
            mapper = getattr(adapter, "map_product", None)
            if mapper is None:
                reviewed[channel] = {"mapped": 0, "unsupported": True}
                continue
            valid = 0
            for product in products:
                payload = {**product, "url": "", "image_url": "", "price_cad": product.get("price_cad", 0)}
                try:
                    result = mapper(payload)
                    valid += not bool(result.get("validation_issues", ()))
                except Exception:
                    pass
            reviewed[channel] = {"mapped": len(products), "valid": valid}
        return {"status": "simulated" if dry_run else "reviewed", "channels": reviewed}

    def op_tax_reserve_review(self, *, dry_run: bool) -> dict[str, Any]:
        from tax.tax_reserve_calculator import tax_reserve
        row = self.container.db.query_one("SELECT COALESCE(SUM(revenue_cad),0) sales FROM orders WHERE financial_status IN ('paid','partially_paid')") or {"sales": 0}
        collected = float(self.container.db.scalar("SELECT COALESCE(SUM(credit-debit),0) FROM ledger WHERE account LIKE '%tax%'", default=0))
        reserve = tax_reserve(float(row["sales"]), 0.05, collected)
        return {"status": "simulated" if dry_run else "reviewed", "taxable_sales_cad": float(row["sales"]), "collected_tax_cad": collected, "minimum_reserve_cad": reserve}

    def op_consent_expiry_review(self, *, dry_run: bool) -> dict[str, Any]:
        rows = self.container.db.query("SELECT purpose,COUNT(*) count FROM customer_consents WHERE granted=1 AND expires_at IS NOT NULL AND expires_at<=datetime('now','+30 days') GROUP BY purpose")
        return {"status": "simulated" if dry_run else "reviewed", "expiring": rows, "count": sum(int(row["count"]) for row in rows)}
