from integrations.shopify.webhooks.handlers.base import make_handler

TOPIC = 'app/scopes_update'
handle = make_handler(topic=TOPIC, action='app_scopes_updated', entity_type='app', id_fields=('admin_graphql_api_id', 'id'), follow_ups=(), required=())
