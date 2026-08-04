from integrations.shopify.webhooks.handlers.base import make_handler

TOPIC = 'app_subscriptions/update'
handle = make_handler(topic=TOPIC, action='app_subscription_updated', entity_type='app_subscription', id_fields=('admin_graphql_api_id', 'id'), follow_ups=(), required=())
