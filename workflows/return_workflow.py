from workflows.base_workflow import ServiceWorkflow


class ReturnWorkflow(ServiceWorkflow):
    name = 'return'
    method_candidates = ('process_return', 'return_order', 'execute', 'run')
