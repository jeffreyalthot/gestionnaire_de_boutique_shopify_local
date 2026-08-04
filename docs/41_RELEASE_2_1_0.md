# Livraison 2.1.0

Cette version approfondit l’architecture cible sans supprimer les composants historiques. Elle privilégie les composants reliés au runtime plutôt que la création de fichiers vides.

## Validation

- `python -m compileall -q .`
- `pytest -q` : 128 tests
- `ctest --test-dir build/native-max` : 4 tests
- `python main.py --validate` : OK en dry-run
- `python main.py --once` : 37 opérations planifiées, 35 mises en file, 2 différées par le budget lourd, aucune erreur

## Limites externes

Les mutations Shopify, commandes/paiements Alibaba, publicités et courriels réels nécessitent des comptes, applications, scopes et autorisations valides. Le code n’invente pas de capacité Alibaba absente du compte et bascule vers l’approbation ou l’exception lorsqu’une capacité n’est pas disponible.
