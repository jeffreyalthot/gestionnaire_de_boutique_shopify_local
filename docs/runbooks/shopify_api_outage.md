# Panne API Shopify

## Déclencheur

Alerte de santé persistante ou erreur de capacité confirmée.

## Procédure

1. Accuser réception locale des webhooks déjà validés.
2. Mettre les mutations en file durable.
3. Limiter les nouvelles recherches de catalogue.
4. Relancer la réconciliation Shopify après rétablissement.

## Critère de sortie

Intégrité validée, files réconciliées et aucune mutation dupliquée.
