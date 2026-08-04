import pytest
from sales_channels.google_merchant_adapter import GoogleMerchantAdapter
from sales_channels.channel_registry import ChannelRegistry
from store_management.page_manager import PageManager
from store_management.metafield_definition_manager import MetafieldDefinitionManager
from store_management.translations_manager import TranslationsManager
from supplier_intelligence.rfq.quote_comparator import QuoteComparator
from supplier_intelligence.samples.sample_quality_review import SampleQualityReview
from tax.tax_engine import TaxEngine
from tax.import_thresholds import ImportThresholds

def product():return {"id":"p1","title":"Produit","description":"D","url":"https://x","image_url":"https://x/i.jpg","price_cad":12.5,"stock":3}
def test_channel_feed_and_registry():
    adapter=GoogleMerchantAdapter();payload=adapter.map_product(product());assert payload["price"]=="12.50 CAD" and not payload["validation_issues"]
    registry=ChannelRegistry();registry.register("google",adapter);assert registry.map_product("google",product())["channel"]=="google_merchant"
def test_store_mutation_plans():
    plan=PageManager().plan("About Us","Body","About Us");assert plan.input["handle"]=="about-us" and len(plan.idempotency_key)==64
    with pytest.raises(ValueError):MetafieldDefinitionManager().definition("x","k","bad")
    assert len(TranslationsManager().plan("gid://shopify/Product/1","fr-CA",{"title":"Titre","empty":""}))==1
def test_supplier_quote_and_sample_review():
    ranked=QuoteComparator().rank([{"supplier_id":"a","landed_unit_cad":10,"lead_time_days":5,"supplier_score":.9},{"supplier_id":"b","landed_unit_cad":20,"lead_time_days":20,"supplier_score":.5}]);assert ranked[0]["supplier_id"]=="a"
    assert SampleQualityReview().review({"material":.9,"function":.8}).passed
def test_tax_engine_and_thresholds():
    result=TaxEngine().calculate(100,"CA","QC");assert result.tax_cad==14.98
    assert ImportThresholds().evaluate(200,100).requires_review
