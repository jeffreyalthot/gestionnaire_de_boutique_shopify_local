# Shopify–Alibaba AI Orchestrator 2.2.0

Version d'approfondissement fonctionnel conservant l'intégralité de la version 2.1.0.

## Nouveautés

- caractéristiques décisionnelles robustes pour clients, commandes, produits, prix, expéditions et fournisseurs;
- comptabilité analytique au cent près avec `Decimal`;
- cache LRU/TTL borné et thread-safe;
- verrou interprocessus portable avec récupération des verrous périmés;
- réception webhook Shopify stricte, bornée, idempotente et enrichie des métadonnées de livraison;
- garde d'ordre des événements et curseur persistant de réconciliation;
- gestion adaptative du coût GraphQL et pagination défensive;
- politiques explicables de confiance, approbation et sécurité;
- calcul dynamique du stock de sécurité et du réapprovisionnement;
- conformité pays/taxes, SEO structuré et campagnes marketing soumises au consentement;
- schémas API Pydantic stricts;
- scanner de secrets compatible avec tous les noms de dossiers de build.

Les validations restent en mode sec et n'effectuent aucune mutation externe réelle.
