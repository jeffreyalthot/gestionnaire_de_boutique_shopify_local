from workflows.base_workflow import ServiceWorkflow


class FulfillmentWorkflow(ServiceWorkflow):
    name = 'fulfillment'
    method_candidates = ('fulfill', 'execute', 'run')
