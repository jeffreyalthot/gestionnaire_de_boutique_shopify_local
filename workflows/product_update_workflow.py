from workflows.base_workflow import ServiceWorkflow


class ProductUpdateWorkflow(ServiceWorkflow):
    name = 'product_update'
    method_candidates = ('update_product', 'update', 'execute', 'run')
