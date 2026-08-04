from workflows.base_workflow import ServiceWorkflow


class CancellationWorkflow(ServiceWorkflow):
    name = 'cancellation'
    method_candidates = ('cancel', 'execute', 'run')
