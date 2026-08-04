from ai.agents.compliance_agent import ComplianceAgent
from ai.agents.pricing_agent import PricingAgent
from ai.models.contextual_bandit import ContextualBandit
from ai.models.demand_forecaster import DemandForecaster
from ai.models.product_ranker import rank_product
from ai.models.supplier_risk_model import assess_supplier_risk
from quality.financial_quality_gate import FinancialQualityGate
from quality.media_quality_gate import MediaQualityGate
from quality.supplier_quality_gate import SupplierQualityGate

def test_policy_agents_block_and_approve():
    assert ComplianceAgent().decide({"restricted_product":True})["blocked"] is True
    assert PricingAgent().decide({"confidence":.99,"margin_score":1,"price_freshness":1})["decision"]=="approve"
def test_models_are_explainable_and_bounded():
    result=rank_product({"quality":1,"supplier":.8,"margin":.9,"stock":.8,"delivery":.8,"demand":.9,"compliance":1})
    assert 0<=result.value<=1 and result.confidence==1
    risk=assess_supplier_risk(.01,.95,5,True,late_rate=.03,quality_score=.9)
    assert risk.value<.4
    forecast=DemandForecaster().forecast([1,2,3,4,5,6,7],7)
    assert forecast.value>0 and forecast.confidence>0
def test_bandit_is_deterministic_and_validated():
    bandit=ContextualBandit(["a","b"],seed=1);first=bandit.choose();bandit.update(first,.8);other=bandit.choose();assert other!=first
    assert bandit.snapshot().total_observations==1
def test_quality_gates():
    assert FinancialQualityGate().evaluate(30,10,2)["allowed"]
    assert not MediaQualityGate().evaluate([{"width":100,"height":100}])["allowed"]
    assert SupplierQualityGate().report(score=.9)["allowed"]
