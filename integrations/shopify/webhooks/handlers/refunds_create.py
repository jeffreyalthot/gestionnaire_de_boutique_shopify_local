from integrations.shopify.webhooks.handlers.base import make_handler

TOPIC = 'refunds/create'
handle = make_handler(topic=TOPIC, action='refund_created', entity_type='refund', id_fields=('admin_graphql_api_id', 'id'), follow_ups=('financial_reconciliation', 'return_refund_review'), required=('id',))
