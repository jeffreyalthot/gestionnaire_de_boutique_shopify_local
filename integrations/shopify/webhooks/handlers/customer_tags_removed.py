from integrations.shopify.webhooks.handlers.base import make_handler

TOPIC = 'customers/tags_removed'
handle = make_handler(topic=TOPIC, action='customer_tags_removed', entity_type='customer', id_fields=('admin_graphql_api_id', 'id'), follow_ups=(), required=())
