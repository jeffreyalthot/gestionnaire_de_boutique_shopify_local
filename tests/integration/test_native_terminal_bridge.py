import json
from infrastructure.native_plan_bridge import NativePlanBridge

def test_native_plan_bridge_ingests_bounded_plan(db,tmp_path):
    plan_dir=tmp_path/"plans"; plan_dir.mkdir()
    (plan_dir/"one.json").write_text(json.dumps({"action":"status","payload":{}}),encoding="utf-8")
    bridge=NativePlanBridge(db,plan_dir)
    result=bridge.ingest_pending(4)
    assert result["scanned"]==0 and result["rejected"]==0
