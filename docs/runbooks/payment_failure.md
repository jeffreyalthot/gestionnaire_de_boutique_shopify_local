# Échec de paiement fournisseur

## Déclencheur

Alerte de santé persistante ou erreur de capacité confirmée.

## Procédure

1. Ne jamais réutiliser une nouvelle clé idempotente pour la même intention.
2. Vérifier l’état distant avant toute nouvelle tentative.
3. Recalculer stock, prix et fret.
4. Escalader lorsque le nombre maximal de tentatives est atteint.

## Critère de sortie

Intégrité validée, files réconciliées et aucune mutation dupliquée.
