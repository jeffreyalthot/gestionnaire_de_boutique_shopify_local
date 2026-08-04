from infrastructure.database.repositories.base_repository import BaseRepository

class PriceRepository(BaseRepository):
    table='price_history'
    id_column='id'
    allowed_columns=frozenset(('product_id', 'supplier_cost', 'shipping_cost', 'sale_price', 'currency', 'reason', 'created_at'))
