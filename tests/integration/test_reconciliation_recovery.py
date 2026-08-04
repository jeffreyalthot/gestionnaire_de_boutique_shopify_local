from app.recovery_manager import RecoveryManager
from infrastructure.queue.durable_queue import DurableQueue

def test_reconciliation_recovery_counts_failed_checkpoints(db):
    db.execute("INSERT INTO reconciliation_checkpoints(name,cursor,status,detail_json,updated_at) VALUES('orders','','failed','{}',datetime('now'))")
    report=RecoveryManager(db,DurableQueue(db)).recover()
    assert report.resumed_checkpoints>=1
