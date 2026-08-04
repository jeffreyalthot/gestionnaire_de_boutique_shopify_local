from pathlib import Path
import pytest
from workflows.order_to_supplier_workflow import OrderToSupplierWorkflow
from tools.generate_status_tree import generate

@pytest.mark.asyncio
async def test_order_supplier_workflow_dry_run_and_gate():
    wf=OrderToSupplierWorkflow()
    payload={"order_id":"o1","paid":True,"expected_profit_cad":10,"risk_score":.1,"lines":[{"quantity":2,"supplier_id":"s1","supplier_sku_id":"sku1"}]}
    result=await wf.execute(payload,dry_run=True,approved=False)
    assert result.status=="waiting_approval" and any(s.status=="simulated" for s in result.steps)
@pytest.mark.asyncio
async def test_order_supplier_workflow_rejects_bad_order():
    result=await OrderToSupplierWorkflow().execute({"order_id":"o","paid":False,"lines":[]},dry_run=True)
    assert result.status=="failed"
def test_status_tree_has_legend(tmp_path: Path):
    root=tmp_path/"p";root.mkdir();(root/"a.py").write_text("def f():\n    return 1\n")
    out=tmp_path/"tree.txt";report=generate(root,out,tmp_path/"status.json")
    text=out.read_text();assert "LÉGENDE DES STATUTS" in text and "a.py" in text and report["files"]==1
