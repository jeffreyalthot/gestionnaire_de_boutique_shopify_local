from workflows.base_workflow import ServiceWorkflow


class ProductUnpublishWorkflow(ServiceWorkflow):
    name = 'product_unpublish'
    method_candidates = ('unpublish', 'execute', 'run')
