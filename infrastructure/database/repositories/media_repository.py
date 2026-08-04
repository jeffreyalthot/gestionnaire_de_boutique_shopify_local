from infrastructure.database.repositories.base_repository import BaseRepository

class MediaRepository(BaseRepository):
    table='media_assets'
    id_column='id'
    allowed_columns=frozenset(('rights_status', 'local_path', 'shopify_media_id', 'status', 'metadata_json', 'updated_at'))
