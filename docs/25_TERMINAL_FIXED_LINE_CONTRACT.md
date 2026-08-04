# Contrat du terminal à lignes fixes

## Objectif

Définir le contrat opérationnel de cette branche sans créer de chemin parallèle au
runtime canonique `Application → AutomationSupervisor → DurableQueue → WorkerSupervisor`.

## Invariants

- Le terminal reste le propriétaire unique de la sortie interactive.
- Les mutations distantes exigent capacité, idempotence, budget et politique.
- Le profil `lite_2gb` limite les requêtes concurrentes à deux et une seule tâche
  lourde par cycle.
- SQLite WAL constitue le journal durable local; les lectures volumineuses sont
  paginées ou traitées en flux.
- Toute reprise commence par une réconciliation de l'état distant.

## Validation minimale

1. Compilation Python complète.
2. Suite `pytest` sans régression.
3. Tests natifs C++ du terminal fixe.
4. Exécution `python main.py --validate` sur une base neuve.
5. Cycle `--once` en mode sec avant toute activation supervisée.
