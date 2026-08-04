from integrations.shopify.webhooks.handlers.base import make_handler

TOPIC = 'products/delete'
handle = make_handler(topic=TOPIC, action='product_deleted', entity_type='product', id_fields=('admin_graphql_api_id', 'id'), follow_ups=('catalog_quality_review', 'sales_channel_review'), required=('id',))
