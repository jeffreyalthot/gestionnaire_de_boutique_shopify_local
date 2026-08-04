from infrastructure.database.repositories.base_repository import BaseRepository

class ExceptionRepository(BaseRepository):
    table='automation_exceptions'
    id_column='id'
    allowed_columns=frozenset(('operation', 'category', 'severity', 'status', 'attempts', 'next_retry_at', 'detail_json', 'updated_at'))
