from infrastructure.queue.durable_queue import DurableQueue

def test_sqlite_queue_handles_small_bounded_batch(db):
    queue=DurableQueue(db)
    for i in range(250): queue.enqueue("bulk",{"i":i},f"bulk:{i}")
    assert queue.stats()["pending"]==250
