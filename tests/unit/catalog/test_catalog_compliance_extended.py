from __future__ import annotations

from catalog.intelligence.niche_ranker import NicheRanker
from catalog.lifecycle.archive_planner import ArchivePlanner
from catalog.media.image_quality_analyzer import ImageQualityAnalyzer
from catalog.media.image_sequence_builder import ImageSequenceBuilder
from catalog.merchandising.smart_tag_engine import SmartTagEngine
from catalog.normalization.barcode_policy import BarcodePolicy
from catalog.normalization.dimension_normalizer import DimensionNormalizer
from catalog.normalization.option_normalizer import OptionNormalizer
from catalog.publishing.draft_builder import DraftBuilder
from catalog.publishing.publication_planner import PublicationPlanner
from compliance.battery_shipping_filter import BatteryShippingFilter
from compliance.compliance_orchestrator import ComplianceOrchestrator
from compliance.image_usage_rights_filter import ImageUsageRightsFilter
from compliance.medical_claim_filter import MedicalClaimFilter
from compliance.quebec_language_filter import QuebecLanguageFilter


def test_niche_ranker_penalizes_saturation():
    ranker = NicheRanker()
    good = ranker.score({"demand": .9, "profitability": .9, "competition": .7,
                         "saturation": .1, "return_risk": .1, "compliance": 1})
    bad = ranker.score({"demand": .9, "profitability": .9, "competition": .7,
                        "saturation": .9, "return_risk": .8, "compliance": 1})
    assert good > bad


def test_archive_planner_preserves_redirect_and_analytics():
    plan = ArchivePlanner().plan({"id": "p1", "stock": 0, "sales_90d": 0, "supplier_active": False})
    assert plan.action == "archive"
    assert plan.preserve_redirect and plan.preserve_analytics


def test_image_quality_and_sequence_are_deduplicated():
    quality = ImageQualityAnalyzer().analyze(width=1200, height=1200, byte_size=100_000,
                                             content_type="image/jpeg")
    assert quality.accepted
    sequence = ImageSequenceBuilder().build([
        {"url": "a", "sha256": "1", "role": "detail", "quality_score": .8},
        {"url": "b", "sha256": "1", "role": "hero", "quality_score": .9},
        {"url": "c", "sha256": "2", "role": "hero", "quality_score": .9},
    ])
    assert len(sequence) == 2
    assert sequence[0]["role"] == "hero"


def test_normalizers_create_shopify_ready_options():
    dimensions = DimensionNormalizer().normalize(10, 20, 30, "in")
    assert dimensions.length_cm == 25.4
    options = OptionNormalizer().normalize({"colour": "grey", "taille": "large"})
    assert options == {"Color": "Gray", "Size": "large"}
    assert BarcodePolicy().evaluate("4006381333931")["allowed"]


def test_draft_and_publication_require_approval():
    draft = DraftBuilder().build({"id": "p1", "title": "Produit", "description": "x" * 200,
                                  "variants": ({"sku": "A"},), "media": ({"url": "x"},)})
    assert draft.fields["status"] == "DRAFT"
    validation = {"passed": True, "failures": ()}
    assert PublicationPlanner().plan(validation=validation, channels=["online"], markets=["CA"])["status"] == "awaiting_approval"


def test_smart_tags_reflect_margin_stock_and_quality():
    tags = SmartTagEngine().build({"category": "Desk", "margin_percent": 55, "stock": 3,
                                   "score": .9, "attributes": {"material": "Wood"}})
    assert {"desk", "high-margin", "low-stock", "featured-candidate", "wood"} <= set(tags)


def test_compliance_orchestrator_blocks_unverified_media_and_claims():
    rights = ImageUsageRightsFilter().evaluate({"source": "supplier"})
    medical = MedicalClaimFilter().evaluate("This product cures pain")
    language = QuebecLanguageFilter().evaluate({"title_fr": "", "description_fr": ""})
    combined = ComplianceOrchestrator().evaluate((
        ("rights", rights), ("medical", medical), ("language", language),
    ))
    assert not combined.passed
    assert combined.review_required
    assert len(combined.findings) >= 3


def test_battery_filter_requires_type_when_battery_included():
    result = BatteryShippingFilter().evaluate({"battery_included": True})
    assert not result.passed
