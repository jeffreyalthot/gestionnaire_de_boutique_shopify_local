# Plan de contrôle commercial

Le `Container` est le propriétaire des services runtime. Les workers reçoivent uniquement des tâches durables, publient leurs résultats sur les bus internes et ne peuvent pas écrire directement dans le terminal.

## Invariants

1. Une intention d’achat possède une clé d’idempotence unique.
2. Une allocation de stock est réalisée dans `BEGIN IMMEDIATE`.
3. Une transition d’achat exige l’état attendu.
4. Une action financière live exige capacité, budget et approbation.
5. Toute opération périodique possède un intervalle et une fenêtre d’idempotence.
6. Le terminal est le seul propriétaire de la console.
7. Les erreurs sont classées, persistées, reprises avec limite puis escaladées.
