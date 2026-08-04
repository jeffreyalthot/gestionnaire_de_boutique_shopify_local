import asyncio
import pytest
from infrastructure.database.engine import Database
from infrastructure.database.checkpoint_manager import CheckpointManager
from infrastructure.database.integrity_checker import IntegrityChecker
from infrastructure.database.query_budget import QueryBudget,QueryBudgetExceeded
from infrastructure.filesystem.atomic_file import atomic_write_text
from infrastructure.http.adaptive_timeout import AdaptiveTimeout
from infrastructure.ipc.message import IpcMessage
from infrastructure.ipc.message_codec import MessageCodec
from infrastructure.queue.backpressure_controller import BackpressureController
from infrastructure.scheduler.job_dependencies import JobDependencies


def test_checkpoint_and_integrity(tmp_path):
    db=Database(tmp_path/'x.db'); db.initialize(); manager=CheckpointManager(db); manager.save('x','1',detail={'a':1})
    assert manager.load('x')['detail']=={'a':1}; assert IntegrityChecker(db).run().ok

def test_query_budget_blocks_excess():
    budget=QueryBudget(max_queries=1); budget.consume()
    with pytest.raises(QueryBudgetExceeded): budget.consume()

def test_atomic_file(tmp_path):
    path=atomic_write_text(tmp_path/'a.txt','hello'); assert path.read_text()=='hello'

def test_adaptive_timeout_is_bounded():
    timeout=AdaptiveTimeout(5,20); timeout.observe(100); assert timeout.value()==20

def test_ipc_codec_roundtrip():
    message=IpcMessage('command',{'x':1}); decoded=MessageCodec.decode(MessageCodec.encode(message)); assert decoded==message

def test_backpressure_rejects_capacity():
    assert BackpressureController(10).decide(10).accept is False

def test_scheduler_detects_cycle():
    deps=JobDependencies(); deps.add('a','b'); deps.add('b','a')
    with pytest.raises(ValueError): deps.validate()
