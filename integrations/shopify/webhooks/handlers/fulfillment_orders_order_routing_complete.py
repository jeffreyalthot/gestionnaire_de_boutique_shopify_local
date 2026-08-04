from integrations.shopify.webhooks.handlers.base import make_handler

TOPIC = 'fulfillment_orders/order_routing_complete'
handle = make_handler(topic=TOPIC, action='order_routing_complete', entity_type='fulfillment_order', id_fields=('admin_graphql_api_id', 'id'), follow_ups=('tracking_reconciliation', 'shopify_fulfillment_sync'), required=())
