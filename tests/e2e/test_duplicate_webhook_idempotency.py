from infrastructure.queue.durable_queue import DurableQueue

def test_duplicate_webhook_enqueues_once(db):
    queue=DurableQueue(db)
    first=queue.enqueue("shopify_webhook",{"id":"w1"},"webhook:w1")
    second=queue.enqueue("shopify_webhook",{"id":"w1"},"webhook:w1")
    assert first==second
    assert db.scalar("SELECT COUNT(*) FROM tasks WHERE idempotency_key='webhook:w1'",default=0)==1
