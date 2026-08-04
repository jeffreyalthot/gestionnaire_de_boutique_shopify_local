from app.recovery_manager import RecoveryManager
from infrastructure.queue.durable_queue import DurableQueue

def test_restart_recovery_reports_database_health(db):
    queue=DurableQueue(db); queue.enqueue("x",{},"restart:x")
    report=RecoveryManager(db,queue).recover()
    assert report.database_ok and report.audit_ok
