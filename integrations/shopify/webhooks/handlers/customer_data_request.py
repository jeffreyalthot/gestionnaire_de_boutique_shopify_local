from integrations.shopify.webhooks.handlers.base import make_handler

TOPIC = 'customers/data_request'
handle = make_handler(topic=TOPIC, action='customer_data_request', entity_type='customer', id_fields=('admin_graphql_api_id', 'id'), follow_ups=(), required=())
