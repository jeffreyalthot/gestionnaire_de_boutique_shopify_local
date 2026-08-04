from infrastructure.queue.durable_queue import DurableQueue
def test_queue_claim_complete(db):
    q=DurableQueue(db); task_id=q.enqueue("x",{"a":1},"key")
    task=q.claim("worker"); assert task and task.id==task_id
    q.complete(task.id); assert q.stats()["completed"]==1
