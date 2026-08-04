from integrations.shopify.webhooks.handlers.base import make_handler

TOPIC = 'fulfillment_orders/cancellation_request_rejected'
handle = make_handler(topic=TOPIC, action='fulfillment_cancellation_rejected', entity_type='fulfillment_order', id_fields=('admin_graphql_api_id', 'id'), follow_ups=('tracking_reconciliation', 'shopify_fulfillment_sync'), required=())
