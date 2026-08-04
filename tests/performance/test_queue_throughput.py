from infrastructure.queue.durable_queue import DurableQueue
def test_small_queue_batch(db):
    q=DurableQueue(db)
    for i in range(20): q.enqueue("x",{"i":i},f"k{i}")
    assert q.stats()["pending"]==20
