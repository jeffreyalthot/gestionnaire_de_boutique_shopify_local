# Récupération SQLite

## Déclencheur

Alerte de santé persistante ou erreur de capacité confirmée.

## Procédure

1. Arrêter les workers et conserver WAL/SHM.
2. Copier la base avant toute réparation.
3. Exécuter quick_check puis integrity_check.
4. Restaurer le dernier backup valide et rejouer les événements idempotents.

## Critère de sortie

Intégrité validée, files réconciliées et aucune mutation dupliquée.
