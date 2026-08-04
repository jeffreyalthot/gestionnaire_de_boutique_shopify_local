from integrations.shopify.webhooks.handlers.base import make_handler

TOPIC = 'fulfillments/update'
handle = make_handler(topic=TOPIC, action='fulfillment_updated', entity_type='fulfillment', id_fields=('admin_graphql_api_id', 'id'), follow_ups=('tracking_reconciliation', 'shopify_fulfillment_sync'), required=('id',))
