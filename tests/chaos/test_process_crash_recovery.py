from infrastructure.queue.durable_queue import DurableQueue

def test_pending_task_survives_process_recreation(db):
    first=DurableQueue(db); task_id=first.enqueue("recover",{"n":1},"crash-safe")
    second=DurableQueue(db); claimed=second.claim("new-process")
    assert claimed and claimed.id==task_id and claimed.payload=={"n":1}
