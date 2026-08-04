from workflows.base_workflow import ServiceWorkflow


class RefundWorkflow(ServiceWorkflow):
    name = 'refund'
    method_candidates = ('refund', 'execute', 'run')
