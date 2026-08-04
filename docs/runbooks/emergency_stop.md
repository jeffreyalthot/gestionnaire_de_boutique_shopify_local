# Arrêt d’urgence

## Déclencheur

Alerte de santé persistante ou erreur de capacité confirmée.

## Procédure

1. Activer le verrouillage global.
2. Suspendre scheduler, workers mutateurs et paiements.
3. Conserver le terminal et les diagnostics en lecture seule.
4. Exiger une validation d’intégrité avant déverrouillage.

## Critère de sortie

Intégrité validée, files réconciliées et aucune mutation dupliquée.
