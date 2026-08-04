import pytest

from workflows.cashflow_protection_workflow import CashflowProtectionWorkflow
from workflows.order_to_supplier_workflow import OrderToSupplierWorkflow
from workflows.product_publication_workflow import ProductPublicationWorkflow
from workflows.supplier_due_diligence_workflow import SupplierDueDiligenceWorkflow


@pytest.mark.asyncio
async def test_mutating_workflow_is_simulated_in_dry_run():
    result = await OrderToSupplierWorkflow().execute({'paid': True, 'order_id': 'o1'}, dry_run=True, approved=True)
    assert result.status == 'completed'
    assert result.steps[-1].status == 'simulated'


@pytest.mark.asyncio
async def test_approval_gate_stops_live_mutation():
    result = await ProductPublicationWorkflow().execute(
        {'quality_score': .9, 'minimum_score': .68, 'media_count': 2}, dry_run=False, approved=False
    )
    assert result.status == 'waiting_approval'
    assert result.steps[-1].status == 'approval_required'


@pytest.mark.asyncio
async def test_cashflow_exposure_is_computed():
    result = await CashflowProtectionWorkflow().execute(
        {'pending_supplier_cad': 100, 'refund_reserve_cad': 25, 'cash_available_cad': 200}, dry_run=True
    )
    assert result.context['exposure_cad'] == 125
    assert result.context['reserve_sufficient'] is True


@pytest.mark.asyncio
async def test_supplier_due_diligence_requires_score():
    result = await SupplierDueDiligenceWorkflow().execute(
        {'company_id': 'c', 'history_score': .5}, dry_run=False, approved=True
    )
    assert result.context['approved_supplier'] is False
