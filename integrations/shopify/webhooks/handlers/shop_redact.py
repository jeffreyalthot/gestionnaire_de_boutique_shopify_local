from integrations.shopify.webhooks.handlers.base import make_handler

TOPIC = 'shop/redact'
handle = make_handler(topic=TOPIC, action='shop_redact', entity_type='shop', id_fields=('admin_graphql_api_id', 'id'), follow_ups=(), required=())
