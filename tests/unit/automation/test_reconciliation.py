from automation.reconciliation.order_reconciler import OrderReconciler

def test_reconciler_module_exposes_order_reconciler():
    assert OrderReconciler.__name__=="OrderReconciler"
