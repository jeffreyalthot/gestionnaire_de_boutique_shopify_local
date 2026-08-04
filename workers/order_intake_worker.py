from workers.specialized_worker import SpecializedWorker


class OrderIntakeWorker(SpecializedWorker):
    name = 'orderintake'
    queue = 'orders'
    accepted_task_types = ('order_intake', 'order_validate', 'order_risk')
