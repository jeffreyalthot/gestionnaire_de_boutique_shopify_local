from infrastructure.database.repositories.base_repository import BaseRepository

class CustomerRepository(BaseRepository):
    table='customer_profiles'
    id_column='customer_id'
    allowed_columns=frozenset(('customer_id', 'risk_level', 'lifetime_value_cad', 'order_count', 'profile_json', 'updated_at'))
