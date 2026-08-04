from infrastructure.database.engine import utcnow
from procurement.batch_builder import BatchBuilder
def test_batch_creation(db):
    batch=BatchBuilder(db).get_or_create_open_batch()
    assert batch["status"]=="open"
