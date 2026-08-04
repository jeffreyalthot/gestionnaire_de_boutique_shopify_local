from infrastructure.queue.durable_queue import DurableQueue
def test_task_survives_new_queue_instance(db):
    DurableQueue(db).enqueue("x",{},"persistent")
    assert DurableQueue(db).claim("new-worker") is not None
