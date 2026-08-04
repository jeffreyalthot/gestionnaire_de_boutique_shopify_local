from integrations.shopify.webhooks.handlers.base import make_handler

TOPIC = 'returns/update'
handle = make_handler(topic=TOPIC, action='return_updated', entity_type='return', id_fields=('admin_graphql_api_id', 'id'), follow_ups=('return_refund_review',), required=('id',))
