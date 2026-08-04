# Rotation des justificatifs

## Déclencheur

Alerte de santé persistante ou erreur de capacité confirmée.

## Procédure

1. Basculer le runtime en mode supervisé sans mutation financière.
2. Créer le nouveau secret dans le fournisseur sécurisé.
3. Tester les capacités en lecture puis en écriture.
4. Révoquer l’ancien secret seulement après validation.

## Critère de sortie

Intégrité validée, files réconciliées et aucune mutation dupliquée.
