from dataclasses import dataclass
from infrastructure.queue.durable_queue import DurableQueue
from infrastructure.queue.poison_message_handler import PoisonMessageHandler

def test_corrupt_plan_is_quarantined(db):
    queue=DurableQueue(db); task_id=queue.enqueue("plan",{"broken":True},"corrupt-plan")
    task=queue.claim("worker"); assert task and task.id==task_id
    PoisonMessageHandler(db).quarantine(task,"invalid plan")
    row=db.query_one("SELECT status,error FROM tasks WHERE id=?",(task_id,))
    assert row["status"]=="dead" and "invalid plan" in row["error"]
