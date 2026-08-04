from workflows.base_workflow import ServiceWorkflow


class InventorySyncWorkflow(ServiceWorkflow):
    name = 'inventory_sync'
    method_candidates = ('sync_inventory', 'sync', 'execute', 'run')
