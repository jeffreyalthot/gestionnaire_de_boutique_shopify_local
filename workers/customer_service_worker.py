from workers.specialized_worker import SpecializedWorker


class CustomerServiceWorker(SpecializedWorker):
    name = 'customerservice'
    queue = 'customer_service'
    accepted_task_types = ('ticket_triage', 'customer_reply', 'ticket_escalation')
