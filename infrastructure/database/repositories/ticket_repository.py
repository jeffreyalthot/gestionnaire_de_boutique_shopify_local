from infrastructure.database.repositories.base_repository import BaseRepository

class TicketRepository(BaseRepository):
    table='customer_tickets'
    id_column='id'
    allowed_columns=frozenset(('category', 'priority', 'status', 'subject', 'context_json', 'updated_at'))
