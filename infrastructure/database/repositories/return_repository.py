from infrastructure.database.repositories.base_repository import BaseRepository

class ReturnRepository(BaseRepository):
    table='return_requests'
    id_column='id'
    allowed_columns=frozenset(('status', 'reason', 'resolution', 'detail_json', 'updated_at'))
