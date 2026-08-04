import pytest
from workflows.base_workflow import BaseWorkflow,WorkflowStep

class RefundDryRun(BaseWorkflow):
    name="refund"
    def steps(self): return (WorkflowStep("validate",lambda c:{"valid":True}),WorkflowStep("refund",lambda c:{"refunded":True},mutating=True))

@pytest.mark.asyncio
async def test_refund_mutation_is_suppressed_in_dry_run():
    result=await RefundDryRun().execute({"order":"o1"},dry_run=True)
    assert [step.status for step in result.steps]==["completed","simulated"]
