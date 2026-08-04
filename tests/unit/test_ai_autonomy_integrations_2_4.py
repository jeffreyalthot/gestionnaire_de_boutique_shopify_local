from __future__ import annotations

import asyncio
from pathlib import Path

import httpx
import pytest

from ai.language.customer_reply_generator import CustomerReplyGenerator
from ai.language.product_copy_generator import ProductCopyGenerator
from ai.language.template_engine import TemplateEngine, TemplateRenderError
from ai.language.text_sanitizer import redact_sensitive, sanitize_html, sanitize_mapping
from ai.language.translation_adapter import TranslationAdapter
from ai.memory.decision_history import DecisionHistory
from ai.memory.error_memory import ErrorMemory
from ai.memory.long_term_memory import LongTermMemory
from ai.memory.short_term_memory import ShortTermMemory
from ai.training.checkpoint_manager import CheckpointManager
from ai.training.drift_detector import DriftDetector
from ai.training.evaluation import binary_metrics, calibration_error, regression_metrics
from ai.training.online_trainer import OnlineTrainer
from ai.training.rollback_manager import RollbackManager
from automation.core.autonomy_controller import AutonomyController
from automation.core.autonomy_kernel import ActionProposal, AutonomyKernel
from automation.policies.rule_policy import RulePolicyDecision
from config.settings import Settings
from integrations.alibaba.gateway import AlibabaGateway
from integrations.shopify.graphql_transport import ShopifyGraphQLTransport


def test_template_engine_required_defaults_and_limits():
    engine=TemplateEngine(); engine.register("hello","Bonjour $name — $suffix",required=("name",),defaults={"suffix":"merci"})
    assert engine.render_named("hello",{"name":"Alex"})=="Bonjour Alex — merci"
    with pytest.raises(TemplateRenderError): engine.render_named("hello",{})
    assert engine.unregister("hello") and not engine.names()


def test_text_sanitizer_removes_html_and_redacts_nested_values():
    assert sanitize_html("<script>x</script><p>Hello&nbsp;world</p>")=="Hello world"
    value=sanitize_mapping({"email":"a@example.com","nested":["+1 514 555 1234"]},redact=True)
    assert value["email"]=="[EMAIL_REDACTED]" and "REDACTED" in value["nested"][0]
    card = "4111 1111 " + "1111 1111"
    assert "PAYMENT" in redact_sensitive(card)


def test_translation_adapter_custom_provider_and_cache():
    adapter=TranslationAdapter(maximum_cache_entries=2)
    adapter.register("en","fr",lambda text,source,target:text.upper(),name="upper")
    first=adapter.translate_with_metadata("hello","en-CA","fr-CA")
    second=adapter.translate_with_metadata("hello","en","fr")
    assert first.text=="HELLO" and not first.cached and second.cached


def test_translation_builtin_dictionary_and_identity():
    adapter=TranslationAdapter()
    assert adapter.translate("hello order","en","fr")=="bonjour commande"
    assert adapter.translate_with_metadata("same","fr","fr").provider=="identity"


def test_customer_reply_and_product_copy_are_deterministic():
    replies=CustomerReplyGenerator()
    assert "TRACK-1" in replies.tracking("A","TRACK-1","https://example.test")
    copy=ProductCopyGenerator().generate("  Blue Widget  ",{"Color":"Blue"},"Useful item")
    assert copy["handle"]=="blue-widget" and len(copy["meta_description"])<=160


def test_long_term_memory_ttl_and_tags(db):
    memory=LongTermMemory(db,namespace="test")
    memory.remember("a",{"x":1},tags=("one","two"))
    assert memory.recall("a")=={"x":1} and memory.record("a").tags==("one","two")
    memory.remember("expired",1,ttl_seconds=0)
    assert memory.recall("expired") is None and not memory.contains("expired")


def test_short_term_memory_eviction_query_and_stats():
    memory=ShortTermMemory(maximum=2)
    memory.add({"type":"a","value":1}); memory.add({"type":"b","value":2}); memory.add({"type":"a","value":3})
    assert len(memory.recent(10))==2
    assert [item["value"] for item in memory.query(type="a")]==[3]
    assert memory.stats()["evicted"]==1


def test_decision_history_and_error_memory(db):
    decisions=DecisionHistory(db); decisions.record_decision("d1",action="publish",confidence=.9); decisions.update_outcome("d1",1)
    assert decisions.success_rate()==1
    errors=ErrorMemory(db); fingerprint=errors.record_error("boom",operation="sync"); errors.record_error("boom",operation="sync")
    assert errors.get(fingerprint)["count"]==2 and errors.unresolved()
    assert errors.resolve(fingerprint) and not errors.unresolved()


def test_checkpoint_manager_integrity_retention_and_promotion(tmp_path: Path):
    manager=CheckpointManager(keep_last=2)
    paths=[]
    for index in range(3): paths.append(manager.save({"index":index},tmp_path/f"model-{index}.joblib",metrics={"score":index}))
    assert len(manager.list(tmp_path))==2
    newest=manager.list(tmp_path)[0]; assert manager.load(newest)["index"] in {1,2}
    active=manager.promote(newest,tmp_path/"active.joblib")
    assert manager.load(active)==manager.load(newest)


def test_checkpoint_manager_detects_tamper(tmp_path: Path):
    manager=CheckpointManager(); path=manager.save({"x":1},tmp_path/"model.joblib")
    path.write_bytes(path.read_bytes()+b"x")
    with pytest.raises(ValueError): manager.load(path)


def test_drift_detector_detects_mean_shift():
    detector=DriftDetector(window=10,threshold=.1,z_threshold=1)
    for value in [0]*5+[1]*5: drift=detector.update(value)
    assert drift and detector.report().recent_mean==1


def test_evaluation_metrics_cover_binary_regression_and_calibration():
    metrics=binary_metrics([1,1,0,0],[1,0,0,0])
    assert metrics["accuracy"]==.75 and metrics["precision"]==1
    regression=regression_metrics([1,2,3],[1,2,4]); assert regression["mae"]>0
    assert 0<=calibration_error([0,1],[.1,.9],bins=2)<=1


class _OnlineModel:
    def __init__(self): self.total=0
    def partial_fit(self,x,y): self.total+=len(x)
    def predict(self,x): return [self.total for _ in x]


def test_online_trainer_batches_and_predicts():
    model=_OnlineModel(); trainer=OnlineTrainer({"m":model},batch_size=2)
    result=trainer.train("m",[1,2,3,4,5],[0,0,0,0,0])
    assert result.batches==3 and trainer.predict("m",[1,2])==[5,5]


def test_rollback_manager_restores_atomic_copy(tmp_path: Path):
    rollback=tmp_path/"rollback.bin"; active=tmp_path/"active.bin"
    rollback.write_bytes(b"good"); active.write_bytes(b"bad")
    result=RollbackManager().rollback(rollback,active)
    assert result.restored and active.read_bytes()==b"good" and result.sha256


class _Capabilities:
    def __init__(self, allowed=True): self.allowed=allowed
    def allows(self, capability, live=False): return self.allowed
class _Governor:
    def __init__(self, allowed=True): self.allowed=allowed
    def allow(self, **kwargs): return self.allowed, "allowed" if self.allowed else "resource_pressure"
class _Lockdown:
    def __init__(self, active=False): self.active=active
    def snapshot(self): return {"active":self.active}


def test_autonomy_kernel_simulates_dry_run_and_counts():
    kernel=AutonomyKernel(capabilities=_Capabilities(),governor=_Governor(),lockdown=_Lockdown(),controller=AutonomyController(dry_run=True))
    decision=kernel.decide(ActionProposal("publish","shopify.product.write",risk="external_write"))
    assert decision.allowed and decision.simulated and kernel.snapshot()["counts"]["simulated"]==1


def test_autonomy_kernel_blocks_policy_and_lockdown():
    kernel=AutonomyKernel(capabilities=_Capabilities(),governor=_Governor(),lockdown=_Lockdown(),controller=AutonomyController(dry_run=False))
    policy=RulePolicyDecision(False,"blocked",approval_required=True)
    decision=kernel.decide(ActionProposal("pay","alibaba.payment",risk="financial",amount_cad=10),policies=(policy,))
    assert not decision.allowed and decision.approval_required and decision.reason=="policy_rejected"
    locked=AutonomyKernel(capabilities=_Capabilities(),governor=_Governor(),lockdown=_Lockdown(True),controller=AutonomyController(dry_run=True))
    assert locked.decide(ActionProposal("x","x")).reason=="emergency_lockdown"


def _live_settings(tmp_path: Path) -> Settings:
    return Settings(app_env="test",app_dry_run=False,app_database_path=tmp_path/"live.db",master_encryption_key="test-key",
        shopify_shop_domain="demo.myshopify.com",shopify_admin_access_token="shop-token",shopify_max_retries=0,
        alibaba_app_key="app",alibaba_app_secret="secret",alibaba_access_token="access",alibaba_max_retries=0)


def test_shopify_transport_records_cost_request_id_and_operation(tmp_path: Path):
    async def run():
        def handler(request: httpx.Request):
            return httpx.Response(200,headers={"X-Request-ID":"req-1"},json={"data":{"shop":{"name":"Demo"}},"extensions":{"cost":{"requestedQueryCost":2,"actualQueryCost":1,"throttleStatus":{"maximumAvailable":1000,"currentlyAvailable":999,"restoreRate":50}}}},request=request)
        client=httpx.AsyncClient(transport=httpx.MockTransport(handler))
        transport=ShopifyGraphQLTransport(_live_settings(tmp_path),client)
        data=await transport.execute("query ShopName { shop { name } }",operation_name="ShopName")
        stats=transport.stats(); await client.aclose(); return data,stats
    data,stats=asyncio.run(run())
    assert data["shop"]["name"]=="Demo" and stats.requests==1 and stats.last_request_id=="req-1" and stats.last_operation=="ShopName"


def test_shopify_transport_rejects_graphql_errors(tmp_path: Path):
    async def run():
        def handler(request): return httpx.Response(200,json={"errors":[{"message":"bad"}]},request=request)
        client=httpx.AsyncClient(transport=httpx.MockTransport(handler)); transport=ShopifyGraphQLTransport(_live_settings(tmp_path),client)
        try:
            with pytest.raises(Exception): await transport.execute("query X { shop { name } }")
        finally: await client.aclose()
        return transport.stats()
    stats=asyncio.run(run()); assert stats.errors==1


def test_alibaba_gateway_records_request_metadata(tmp_path: Path):
    async def run():
        def handler(request: httpx.Request):
            assert b"method=test.method" in request.content
            return httpx.Response(200,headers={"x-request-id":"header-id"},json={"test_method_response":{"request_id":"body-id","result":{"ok":True}}},request=request)
        client=httpx.AsyncClient(transport=httpx.MockTransport(handler)); gateway=AlibabaGateway(_live_settings(tmp_path),client)
        payload=await gateway.call("test.method",{"product_id":"1"}); stats=gateway.stats(); await client.aclose(); return payload,stats
    payload,stats=asyncio.run(run())
    assert "test_method_response" in payload and stats.requests==1 and stats.last_request_id=="body-id"


def test_alibaba_gateway_rejects_empty_method(tmp_path: Path):
    async def run():
        client=httpx.AsyncClient(transport=httpx.MockTransport(lambda request:httpx.Response(200,json={},request=request)))
        gateway=AlibabaGateway(_live_settings(tmp_path),client)
        try:
            with pytest.raises(ValueError): await gateway.call(" ")
        finally: await client.aclose()
    asyncio.run(run())
