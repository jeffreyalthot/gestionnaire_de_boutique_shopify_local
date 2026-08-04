from workflows.base_workflow import ServiceWorkflow


class ProductDiscoveryWorkflow(ServiceWorkflow):
    name = 'product_discovery'
    method_candidates = ('discover_products', 'discover', 'execute', 'run')
