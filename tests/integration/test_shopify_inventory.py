from inventory.inventory_reconciler import InventoryReconciler
def test_inventory_reconcile(): assert InventoryReconciler().compare(5,10,2)["desired"]==8
