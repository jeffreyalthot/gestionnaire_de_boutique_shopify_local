# Panne API Alibaba

## Déclencheur

Alerte de santé persistante ou erreur de capacité confirmée.

## Procédure

1. Activer le mode lecture locale et suspendre les créations de commandes.
2. Conserver les intentions d’achat avec leur clé d’idempotence.
3. Vérifier les capacités OAuth et la limite de débit.
4. Relancer une réconciliation avant toute reprise de paiement.

## Critère de sortie

Intégrité validée, files réconciliées et aucune mutation dupliquée.
