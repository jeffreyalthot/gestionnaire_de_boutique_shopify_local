from __future__ import annotations

from analytics.anomaly.base import RobustAnomalyDetector
from analytics.attribution.channel_attribution import ChannelAttribution
from analytics.collector import AnalyticsCollector
from analytics.event_facts import EventFact
from analytics.scorecards.store_scorecard import StoreScorecard
from finance.cash_reserve_policy import CashReservePolicy
from finance.cashflow_forecast import CashflowForecast
from finance.chart_of_accounts import ChartOfAccounts
from finance.marketing_budget import MarketingBudget
from finance.transaction_matcher import TransactionMatcher


def test_robust_anomaly_detector_flags_extreme_value():
    result = RobustAnomalyDetector().detect([10, 11, 10, 9, 10, 11, 10], 100)
    assert result.anomalous


def test_channel_attribution_conserves_revenue():
    allocation = ChannelAttribution().allocate(
        [{"channel": "search"}, {"channel": "email"}, {"channel": "direct"}],
        100.0,
        model="position_based",
    )
    assert round(sum(allocation.values()), 2) == 100.0
    assert allocation["search"] == 40.0


def test_analytics_collector_persists_dimensioned_fact(db):
    collector = AnalyticsCollector(db)
    collector.record(EventFact("conversion_rate", 0.12, {"store": "main", "unknown": "discard"}))
    series = collector.series("conversion_rate")
    assert series[0]["value"] == 0.12
    assert series[0]["dimensions"] == {"store": "main"}


def test_store_scorecard_returns_grade():
    score = StoreScorecard().build({"profitability": .9, "fulfillment": .8, "customer": .9,
                                    "compliance": 1.0, "reliability": 1.0})
    assert score.grade in {"A", "B"}


def test_cash_reserve_protects_marketing_budget():
    reserve = CashReservePolicy().calculate(
        trailing_refunds_cad=100, trailing_chargebacks_cad=50,
        pending_supplier_payments_cad=500, fixed_operating_cost_cad=100,
    )
    budget = MarketingBudget().allocate(
        available_cash_cad=1000,
        reserve_required_cad=reserve["required_reserve_cad"],
        trailing_profit_cad=1000,
    )
    assert budget["budget_cad"] <= 62.5


def test_cashflow_forecast_is_bounded_to_horizon():
    result = CashflowForecast().forecast([100, 120, 80], [50, 60, 70], horizon=5)
    assert len(result["net"]) == 5
    assert len(result["cumulative"]) == 5


def test_transaction_matcher_prefers_exact_reference():
    matcher = TransactionMatcher()
    result = matcher.best(
        {"amount": 100, "currency": "CAD", "reference": "A", "date": "2026-07-01"},
        [
            {"amount": 100, "currency": "CAD", "reference": "B", "date": "2026-07-01"},
            {"amount": 100, "currency": "CAD", "reference": "A", "date": "2026-07-01"},
        ],
    )
    assert result["transaction"]["reference"] == "A"


def test_chart_of_accounts_has_balanced_categories():
    accounts = ChartOfAccounts().all()
    assert any(item.category == "asset" for item in accounts)
    assert any(item.category == "revenue" for item in accounts)
    assert any(item.category == "expense" for item in accounts)
