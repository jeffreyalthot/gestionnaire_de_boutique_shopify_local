from infrastructure.database.repositories.base_repository import BaseRepository

class AnalyticsRepository(BaseRepository):
    table='analytics_facts'
    id_column='id'
    allowed_columns=frozenset(('dimensions_json', 'captured_at', 'metric', 'value'))
