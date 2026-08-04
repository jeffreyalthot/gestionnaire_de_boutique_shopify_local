from infrastructure.database.repositories.base_repository import BaseRepository

class PolicyRepository(BaseRepository):
    table='automation_policy_decisions'
    id_column='id'
    allowed_columns=frozenset(('decision', 'reason', 'detail_json', 'created_at'))
