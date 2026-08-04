from integrations.shopify.webhooks.handlers.base import make_handler

TOPIC = 'inventory_levels/update'
handle = make_handler(topic=TOPIC, action='inventory_updated', entity_type='inventory_level', id_fields=('inventory_item_id', 'location_id', 'id'), follow_ups=('inventory_reconciliation',), required=())
