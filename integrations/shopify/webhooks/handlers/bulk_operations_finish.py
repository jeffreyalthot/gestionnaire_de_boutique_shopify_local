from integrations.shopify.webhooks.handlers.base import make_handler

TOPIC = 'bulk_operations/finish'
handle = make_handler(topic=TOPIC, action='bulk_operation_finished', entity_type='bulk_operation', id_fields=('admin_graphql_api_id', 'id'), follow_ups=(), required=())
