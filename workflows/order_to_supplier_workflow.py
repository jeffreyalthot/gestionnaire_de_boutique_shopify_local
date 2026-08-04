from __future__ import annotations
from hashlib import sha256
from typing import Any,Iterable
from workflows.base_workflow import BaseWorkflow,WorkflowStep,WorkflowError

class OrderToSupplierWorkflow(BaseWorkflow):
    name="order_to_supplier"
    def steps(self) -> Iterable[WorkflowStep]:
        return (WorkflowStep("validate_paid_order",self._validate),WorkflowStep("risk_and_margin_gate",self._gate),WorkflowStep("reserve_inventory",self._reserve,mutating=True),WorkflowStep("build_purchase_intent",self._intent,mutating=True),WorkflowStep("submit_supplier_order",self._submit,mutating=True,approval_required=True))
    def _validate(self,ctx: dict[str,Any]) -> dict[str,Any]:
        issues=[]
        if not ctx.get("order_id"):issues.append("missing_order_id")
        if not ctx.get("paid",False):issues.append("order_not_paid")
        raw_lines=ctx.get("lines")
        lines=[] if raw_lines is None else raw_lines
        if not isinstance(lines,list):issues.append("invalid_lines");lines=[]
        for i,line in enumerate(lines):
            if int(line.get("quantity",0) or 0)<=0:issues.append(f"line_{i}_invalid_quantity")
            if not line.get("supplier_id") or not line.get("supplier_sku_id"):issues.append(f"line_{i}_supplier_mapping_missing")
        if issues:raise WorkflowError(",".join(issues))
        return {"order_valid":True,"validated_line_count":len(lines)}
    def _gate(self,ctx: dict[str,Any]) -> dict[str,Any]:
        risk=float(ctx.get("risk_score",0) or 0);limit=float(ctx.get("max_risk_score",.65) or .65);floor=float(ctx.get("minimum_profit_cad",1) or 1)
        if risk>limit:raise WorkflowError("order_risk_above_limit")
        if "expected_profit_cad" in ctx and float(ctx.get("expected_profit_cad",0) or 0)<floor:raise WorkflowError("expected_profit_below_floor")
        return {"risk_gate_passed":True,"margin_gate_passed":True}
    def _reserve(self,ctx: dict[str,Any]) -> dict[str,Any]:
        lines=ctx.get("lines") or [];units=sum(int(line.get("quantity",0) or 0) for line in lines);return {"inventory_reserved":True,"reserved_units":units}
    def _intent(self,ctx: dict[str,Any]) -> dict[str,Any]:
        lines=ctx.get("lines") or []
        key=sha256(f"{ctx['order_id']}|{repr(sorted((line.get('supplier_sku_id'),line.get('quantity')) for line in lines))}".encode()).hexdigest()
        groups={}
        for line in lines:groups.setdefault(str(line["supplier_id"]),[]).append(dict(line))
        return {"purchase_intent_created":True,"purchase_intent_key":key,"supplier_groups":groups}
    def _submit(self,ctx: dict[str,Any]) -> dict[str,Any]:
        if not ctx.get("purchase_intent_created"):raise WorkflowError("purchase_intent_missing")
        return {"supplier_order_submitted":True,"submitted_supplier_count":len(ctx.get("supplier_groups",{}))}
