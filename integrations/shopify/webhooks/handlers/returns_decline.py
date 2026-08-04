from integrations.shopify.webhooks.handlers.base import make_handler

TOPIC = 'returns/decline'
handle = make_handler(topic=TOPIC, action='return_declined', entity_type='return', id_fields=('admin_graphql_api_id', 'id'), follow_ups=('return_refund_review',), required=('id',))
