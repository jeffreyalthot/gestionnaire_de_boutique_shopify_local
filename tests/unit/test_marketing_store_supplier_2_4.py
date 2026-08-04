from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

import pytest

from compliance.counterfeit_risk_filter import CounterfeitRiskFilter
from compliance.customs_compliance import CustomsCompliance
from compliance.dangerous_goods_filter import DangerousGoodsFilter
from compliance.trademark_filter import TrademarkFilter
from finance.chargeback_reserve import ChargebackReservePolicy
from finance.duty_reserve import DutyReservePolicy
from finance.profit_by_dimension import ProfitDimensionAnalyzer
from finance.tax_reserve import TaxReservePolicy
from marketing.automatic_discount_manager import AutomaticDiscountManager
from marketing.content.blog_planner import BlogPlanner
from marketing.content.brand_voice_policy import BrandVoicePolicy
from marketing.content.page_content_manager import PageContentManager
from marketing.content.product_content_auditor import ProductContentAuditor
from marketing.customer_segment_targeting import CustomerSegmentTargeting
from marketing.discount_code_manager import DiscountCodeManager
from marketing.email.abandoned_checkout_flow import AbandonedCheckoutFlow
from marketing.email.campaign_builder import CampaignBuilder
from marketing.email.customer_journey import CustomerJourney
from marketing.email.post_purchase_flow import PostPurchaseFlow
from marketing.free_shipping_policy import FreeShippingPolicy
from marketing.promotion_calendar import PromotionCalendar
from marketing.seo.internal_link_builder import InternalLinkBuilder
from marketing.seo.meta_description_builder import MetaDescriptionBuilder
from marketing.seo.meta_title_builder import MetaTitleBuilder
from marketing.seo.seo_auditor import SEOAuditor
from marketing.seo.url_handle_builder import UrlHandleBuilder
from store_management.domain_auditor import DomainAuditor
from store_management.markets_manager import MarketsManager
from store_management.menu_manager import MenuManager
from store_management.payment_settings_audit import PaymentSettingsAudit
from store_management.redirect_manager import RedirectManager
from store_management.settings_sync import StoreSettingsSync
from store_management.shipping_settings_audit import ShippingSettingsAudit
from store_management.tax_settings_audit import TaxSettingsAudit
from store_management.theme_asset_guard import ThemeAssetGuard
from store_management.theme_settings_manager import ThemeSettingsManager
from supplier_intelligence.due_diligence.certification_verifier import CertificationVerifier
from supplier_intelligence.due_diligence.company_verifier import CompanyVerifier
from supplier_intelligence.due_diligence.credential_verifier import CredentialVerifier
from supplier_intelligence.rfq.negotiation_policy import NegotiationPolicy
from supplier_intelligence.rfq.quote_normalizer import QuoteNormalizer
from supplier_intelligence.rfq.rfq_builder import RFQBuilder
from supplier_intelligence.samples.sample_tracker import SampleTracker
from supplier_intelligence.supplier_blacklist import SupplierBlacklist
from supplier_intelligence.supplier_candidate import SupplierCandidate
from supplier_intelligence.supplier_discovery import SupplierDiscovery
from supplier_intelligence.supplier_dispute_history import SupplierDisputeHistory
from supplier_intelligence.supplier_profile import SupplierProfile
from supplier_intelligence.supplier_repository import SupplierRepository
from supplier_intelligence.supplier_risk_assessor import SupplierRiskAssessor
from supplier_intelligence.supplier_watchlist import SupplierWatchlist


def test_reserve_policies_are_explainable():
    assert ChargebackReservePolicy().evaluate(1000,.02).reserve_cad > 20
    assert DutyReservePolicy().evaluate(1000,.05).reserve_cad == 60
    tax=TaxReservePolicy().evaluate(100,20,5,buffer_percent=10)
    assert tax.payable_cad==85 and tax.reserve_cad>85


def test_profit_dimension_analyzer_calculates_margin_and_share():
    rows=[{"channel":"online","order_id":"1","revenue_cad":100,"profit_cad":30},{"channel":"pos","order_id":"2","revenue_cad":50,"profit_cad":10}]
    result=ProfitDimensionAnalyzer().analyze(rows,"channel")
    assert result[0].key=="online" and result[0].margin_percent==30 and result[0].share_percent==75


def test_compliance_filters_return_structured_decisions():
    assert CustomsCompliance().evaluate("A","123456","CA",10).valid
    assert TrademarkFilter().assess("Nike style",{"Nike"}).blocked
    assert CounterfeitRiskFilter().assess("1:1 replica with logo").blocked
    goods=DangerousGoodsFilter().assess("lithium battery pack")
    assert goods.carrier_review_required and goods.shipping_mode=="ground_only"


def test_page_and_blog_planning_are_deterministic():
    page=PageContentManager().prepare(" About us ","<p>Hello</p>")
    assert page.handle=="about-us" and page.fingerprint
    plan=BlogPlanner().detailed_plan(["best widget","guide widget"],["p1"],limit=2,start=date(2026,1,1))
    assert plan[0].intent=="commercial" and plan[1].publish_date=="2026-01-08"


def test_segment_post_purchase_and_journey_guards():
    target=CustomerSegmentTargeting().evaluate({"vip","canada"},{"vip"},{"fraud"})
    assert target.eligible
    assert PostPurchaseFlow().next_message(7)=="review_request"
    journey=CustomerJourney().evaluate(orders=2,days_since_order=130,consent=False)
    assert journey.stage=="winback" and not journey.automation_allowed


def test_free_shipping_and_abandoned_checkout_respect_profit_and_consent():
    assert FreeShippingPolicy().eligible(subtotal_cad=100,shipping_cad=8,gross_profit_cad=20)
    steps=AbandonedCheckoutFlow().plan(2000,consent=False)
    assert all(not step.allowed for step in steps)


def test_seo_builders_auditor_and_internal_links():
    assert MetaTitleBuilder().build("A useful product title",brand="ELIT21").endswith("ELIT21")
    assert len(MetaDescriptionBuilder().build("word "*100))<=160
    handle=UrlHandleBuilder().build_details("Café Bleu",existing={"cafe-bleu"})
    assert handle.collision_suffix
    links=InternalLinkBuilder().rank({"blue","widget"},[{"url":"/p","tags":["widget"],"title":"P"}])
    assert links[0].url=="/p"
    audit=SEOAuditor().evaluate(title="T"*40,description="D"*100,handle="valid-handle")
    assert audit.valid


def test_brand_voice_product_content_and_campaign_builder():
    assert not BrandVoicePolicy().assess("best in the world").valid
    audit=ProductContentAuditor().evaluate({"title":"Short useful product","description":"Description "*20,"handle":"short-useful-product","images":["x"],"vendor":"v"})
    assert audit.score>0
    campaign=CampaignBuilder().prepare(name="Launch",subject="Hello",body="Body "*30,segment="vip")
    assert campaign.status=="draft" and campaign.fingerprint


def test_discount_code_and_automatic_discount():
    manager=DiscountCodeManager(); code=manager.generate("ELIT",6)
    assert manager.valid(code)
    proposal=AutomaticDiscountManager().evaluate({"id":"p","price_cad":100,"landed_cost_cad":60,"fees_cad":5},50)
    assert proposal.applied_percent<=proposal.safe_maximum_percent


def test_promotion_calendar_finds_next_slot():
    calendar=PromotionCalendar({date(2026,1,2)})
    assert not calendar.available(date(2026,1,1),date(2026,1,3),[])
    slot=calendar.next_available(date(2026,1,1),2,[])
    assert slot[0]>=date(2026,1,3)


def test_store_markets_menus_domains_and_redirects():
    markets=MarketsManager().audit([{"name":"Canada","countries":["CA"],"currency":"CAD","languages":["fr-CA"]}])
    assert markets[0].valid and MarketsManager().routing_table([{"name":"Canada","countries":["CA"],"currency":"CAD"}])["CA"]=="Canada"
    assert MenuManager().audit([{"title":"Home","url":"/","children":[]}]).valid
    assert DomainAuditor().evaluate("https://example.com","example.com").valid
    redirects=RedirectManager(); assert redirects.plan("old","new").safe
    assert redirects.detect_cycles([("/a","/b"),("/b","/a")])


def test_store_settings_and_audits():
    sync=StoreSettingsSync(); plan=sync.plan({"name":"New","currency":"CAD","secret":"x"},{"name":"Old","currency":"USD"})
    assert len(plan.changes)==2 and "secret" in plan.ignored
    applied=sync.apply({"name":"Old","currency":"USD"},plan,approved=False)
    assert applied["name"]=="New" and applied["currency"]=="USD"
    assert PaymentSettingsAudit().evaluate({"currency":"CAD","providers":["shopify"]}).valid
    assert ShippingSettingsAudit().evaluate([{"countries":["CA"],"rates":[{"price":5}]}]).valid
    assert TaxSettingsAudit().evaluate({"prices_include_tax":False,"home_country":"CA","registrations":["GST"]}).valid


def test_theme_guard_and_settings_patch():
    content=b"body{}"; decision=ThemeAssetGuard().inspect("assets/app.css",len(content),content=content)
    assert decision.allowed and decision.sha256
    plan=ThemeSettingsManager().plan({"color":"red"},{"color":"blue"},{"color"})
    assert plan.changed==("color",) and plan.result["color"]=="blue"


def test_company_credentials_and_certifications():
    company=CompanyVerifier().evaluate({"legal_name":"Acme","registration_id":"1","country_code":"CA"})
    assert company.valid
    credentials=CredentialVerifier().evaluate({"license":{"identifier":"L","expires_on":"2999-01-01"}})
    assert credentials.valid
    cert=CertificationVerifier().evaluate({"issuer":"ISO","identifier":"1","expires_on":"2999-01-01"})
    assert cert.valid


def test_rfq_quote_and_negotiation():
    rfq=RFQBuilder().create(sku="a",quantity=100,destination_country="CA")
    assert rfq.status=="draft" and rfq.idempotency_key
    quote=QuoteNormalizer().evaluate({"supplier_id":"s","unit_price":10,"freight":100,"quantity":100,"moq":50},rate_to_cad=1.2)
    assert quote.valid and quote.landed_unit_cad>quote.unit_price_cad
    target=NegotiationPolicy().plan(quoted_unit_cad=12,benchmark_unit_cad=10,quantity=500)
    assert target.target_unit_cad<10


def test_sample_tracker_validates_transitions():
    tracker=SampleTracker(); tracker.update("s","ordered");tracker.update("s","shipped",tracking="t")
    assert tracker.get("s")["tracking"]=="t" and len(tracker.history("s"))==2
    with pytest.raises(ValueError): tracker.update("s","planned")


def test_supplier_repository_watchlist_blacklist_and_discovery():
    repo=SupplierRepository();repo.save(SupplierProfile("s","Supplier",.8,"approved",country_code="CN"))
    assert repo.search("supplier")[0].supplier_id=="s"
    watch=SupplierWatchlist();watch.add("s","late");watch.add("s","late again");assert watch.details()[0]["occurrences"]==2
    blacklist=SupplierBlacklist();blacklist.add("b","fraud");assert blacklist.blocked("b")
    with pytest.raises(PermissionError):blacklist.remove("b",authorized=False)
    candidates=[SupplierCandidate("a","A","CN",2,verified=True),SupplierCandidate("b","B","US",2,verified=True)]
    result=SupplierDiscovery().evaluate(candidates,countries={"CN"})
    assert [x.supplier_id for x in result.accepted]==["a"]


def test_supplier_dispute_and_risk_assessment():
    metrics=SupplierDisputeHistory().summarize([{"outcome":"won","resolution_days":2}],orders=10)
    assert metrics.dispute_rate==.1 and metrics.won_rate==1
    risk=SupplierRiskAssessor().assess({"verified":False,"trade_assurance":False,"years_active":0,"dispute_rate":.1,"blacklisted":True})
    assert risk.level=="critical" and risk.recommended_action=="block"
