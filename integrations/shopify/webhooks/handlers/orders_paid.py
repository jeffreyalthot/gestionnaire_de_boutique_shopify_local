from integrations.shopify.webhooks.handlers.base import make_handler

TOPIC = 'orders/paid'
handle = make_handler(topic=TOPIC, action='order_paid', entity_type='order', id_fields=('admin_graphql_api_id', 'id'), follow_ups=('order_risk_review', 'supplier_order_planning'), required=('id',))
