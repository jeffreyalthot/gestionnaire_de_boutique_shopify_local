# Sécurité

Les secrets ne doivent jamais être commités. Le runtime refuse de conserver un
numéro de carte, un CVV ou un NIP. Les paiements Alibaba utilisent une session
OAuth et un moyen de paiement autorisé dans le compte Alibaba. Les webhooks
Shopify sont validés par HMAC sur le corps brut. Toutes les actions externes
utilisent une clé d'idempotence et sont journalisées.
