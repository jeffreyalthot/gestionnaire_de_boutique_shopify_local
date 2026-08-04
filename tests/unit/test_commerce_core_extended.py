from __future__ import annotations

from datetime import datetime, timedelta, timezone

from inventory.inventory_allocation import InventoryAllocation
from inventory.inventory_position import InventoryPosition
from inventory.inventory_snapshot_repository import InventorySnapshotRepository
from marketing.campaign import Campaign
from marketing.campaign_guardrails import CampaignGuardrails
from marketing.discount_optimizer import DiscountOptimizer
from marketing.seo.url_handle_builder import UrlHandleBuilder
from orders.order_intake import OrderIntake
from orders.order_profit_snapshot import OrderProfitSnapshot
from orders.order_splitter import OrderSplitter
from orders.order_timeline import OrderTimeline
from pricing.price_history import PriceHistory
from pricing.profit_floor_guard import ProfitFloorGuard
from procurement.payment_budget_guard import PaymentBudgetGuard
from procurement.purchase_intent import PurchaseIntent
from procurement.purchase_intent_repository import PurchaseIntentRepository
from procurement.purchase_plan import PurchasePlan
from procurement.purchase_plan_validator import PurchasePlanValidator
from risk.fraud.high_risk_order_gate import HighRiskOrderGate
from risk.fraud.order_fraud_rules import OrderFraudRules
from security.download_scanner import DownloadScanner
from security.oauth_state_store import OAuthStateStore
from security.session_integrity import SessionIntegrity


def test_order_intake_normalizes_and_validates():
    raw={"id":"1","total":"12.345","currency":"cad","shipping_address":{"address1":"  1 rue test ","city":"Montréal","country_code":"CA","postal_code":"H2X 1Y4"},"lines":[{"sku":" abc ","quantity":1}]}
    result=OrderIntake().process(raw)
    assert result.accepted
    assert result.order["currency"]=="CAD"
    assert result.order["lines"][0]["sku"]=="ABC"


def test_order_splitter_and_profit_snapshot():
    groups=OrderSplitter().by_supplier([{"supplier_id":"s1","sku":"a"},{"supplier_id":"s2","sku":"b"},{"supplier_id":"s1","sku":"c"}])
    assert len(groups["s1"])==2
    snapshot=OrderProfitSnapshot(100,40,10,5,3)
    assert snapshot.profit_cad==42
    assert snapshot.margin_percent==42


def test_order_timeline_persists(db):
    timeline=OrderTimeline(db)
    timeline.append("o1","order_held",status="held",detail={"reason":"risk"})
    rows=timeline.list("o1")
    assert rows[0]["detail"]["reason"]=="risk"


def test_inventory_allocation_is_atomic_and_prevents_oversell(db):
    repo=InventorySnapshotRepository(db)
    repo.upsert(InventoryPosition("SKU",on_hand=5,safety_stock=1))
    allocation=InventoryAllocation(db)
    assert allocation.allocate("SKU",3).allocated
    denied=allocation.allocate("SKU",2)
    assert not denied.allocated and denied.reason=="insufficient_stock"
    assert allocation.release("SKU",2)==1


def test_price_history_and_profit_floor(db):
    history=PriceHistory(db)
    history.record("product","p1",price_cad=20,landed_cost_cad=10,source="supplier")
    assert history.latest("product","p1")["margin_percent"]==50
    assert ProfitFloorGuard(min_profit_cad=3,min_margin_percent=20).evaluate(price_cad=20,landed_cost_cad=10).allowed


def test_purchase_intent_repository_idempotency(db):
    repo=PurchaseIntentRepository(db)
    intent=PurchaseIntent("i1","order:o1:s1","o1","s1",25,lines=({"sku":"A"},))
    assert repo.create(intent)
    assert not repo.create(PurchaseIntent("i2","order:o1:s1","o1","s1",25))
    assert repo.transition("i1","planned","approved")
    assert not repo.transition("i1","planned","approved")


def test_purchase_plan_validation_and_budget_guard():
    intent=PurchaseIntent("i","k","o","s",20)
    plan=PurchasePlan("o",(intent,),20,1)
    assert PurchasePlanValidator().validate(plan,financial_limit_cad=100).valid
    assert PaymentBudgetGuard().evaluate(requested_cad=20,spent_today_cad=30,daily_budget_cad=100,reserve_cad=50,cash_cad=100)[0]
    assert not PaymentBudgetGuard().evaluate(requested_cad=60,spent_today_cad=50,daily_budget_cad=100,reserve_cad=0,cash_cad=200)[0]


def test_fraud_gate_blocks_high_risk_order():
    score=OrderFraudRules().assess({"proxy_or_vpn":True,"billing_shipping_mismatch":True,"high_risk_country":True,"total_amount":1000})
    decision=HighRiskOrderGate().evaluate(score)
    assert decision.action in {"hold","block"}
    assert not decision.allowed


def test_oauth_state_single_use_and_session_integrity(db):
    states=OAuthStateStore(db)
    state=states.issue("shopify")
    assert states.consume(state,"shopify")
    assert not states.consume(state,"shopify")
    integrity=SessionIntegrity(b"0123456789abcdef0123456789abcdef")
    payload={"operator":"local","expires":123}
    signature=integrity.sign(payload)
    assert integrity.verify(payload,signature)
    assert not integrity.verify({**payload,"expires":124},signature)


def test_download_scanner_validates_magic_and_content_type():
    png=b"\x89PNG\r\n\x1a\n"+b"0"*20
    result=DownloadScanner().scan(png,claimed_type="image/png")
    assert result.safe
    assert not DownloadScanner().scan(png,claimed_type="image/jpeg").safe


def test_campaign_guardrails_and_safe_discount():
    now=datetime.now(timezone.utc)
    campaign=Campaign("c","Summer","email",50,now,now+timedelta(days=1))
    assert CampaignGuardrails().validate(campaign,available_budget_cad=100).allowed
    assert not CampaignGuardrails().validate(campaign,available_budget_cad=10).allowed
    assert DiscountOptimizer().maximum_safe_discount(regular_price_cad=100,landed_cost_cad=50)>0


def test_url_handle_builder():
    assert UrlHandleBuilder().build("Étagère de Cuisine – Grande") == "etagere-de-cuisine-grande"
