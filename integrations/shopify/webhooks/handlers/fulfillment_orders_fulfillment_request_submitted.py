from integrations.shopify.webhooks.handlers.base import make_handler

TOPIC = 'fulfillment_orders/fulfillment_request_submitted'
handle = make_handler(topic=TOPIC, action='fulfillment_request_submitted', entity_type='fulfillment_order', id_fields=('admin_graphql_api_id', 'id'), follow_ups=('tracking_reconciliation', 'shopify_fulfillment_sync'), required=())
