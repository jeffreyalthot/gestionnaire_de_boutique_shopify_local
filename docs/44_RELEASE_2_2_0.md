# Version 2.2.0 — approfondissement du moteur autonome

Cette version conserve l'architecture 2.1.0 et approfondit les modules exécutés plutôt que d'ajouter des coquilles.

## Changements principaux

- extraction de caractéristiques robuste pour clients, commandes, produits, prix, fournisseurs et expéditions;
- calculs financiers au cent près avec `Decimal` et rapports détaillés de marge, réserve et variance;
- cache LRU/TTL borné, thread-safe, avec statistiques et pression mémoire;
- verrou interprocessus portable, temporisé et récupérable après verrou périmé;
- validation webhook HMAC stricte sur le corps brut, limite de taille et enveloppe de métadonnées complète;
- garde d'ordre des webhooks et curseur persistant de réconciliation avec chevauchement;
- budget GraphQL adaptatif basé sur `throttleStatus` et coût calculé;
- pagination protégée contre les curseurs absents, les boucles et les volumes non bornés;
- politiques de confiance, approbation et sécurité explicables;
- stock de sécurité dynamique, point de commande et quantité de réapprovisionnement;
- schémas API Pydantic stricts et campagnes marketing soumises au consentement;
- correction du scanner de secrets pour tous les dossiers de build nommés.

Aucune mutation Shopify ou Alibaba réelle n'est exécutée pendant les validations.
