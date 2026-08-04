# Shopify–Alibaba Terminal Orchestrator 2.4.0

Cette version approfondit la version 2.3.0 sans supprimer aucun fichier antérieur ni remplacer l’architecture canonique.

## Développements

- agents et modèles faibles ressources explicables ;
- mémoire SQLite TTL, historique, tags et métriques ;
- checkpoints atomiques compressés avec SHA-256, promotion et rollback ;
- gouvernance centrale de l’autonomie, des capacités, du risque et des ressources ;
- transports Shopify GraphQL et Alibaba instrumentés et bornés ;
- calculs financiers Decimal, réserves et profit par dimension ;
- catalogue, médias, normalisation, publication, SEO et merchandising ;
- inventaire multi-emplacement, sécurité de stock, backorder et preorder ;
- achats fournisseurs idempotents, paiements, annulation, suivi et compensation ;
- fulfillment, notifications, retours, remboursements, litiges et chargebacks ;
- marketing, gestion de boutique, fiscalité, conformité et fournisseurs ;
- observabilité, rapports, alertes, incidents, workers et santé SQLite ;
- terminal C++17 à lignes fixes conservé.

## Validation

Toutes les validations sont effectuées en mode sec ou au moyen de transports simulés. Aucune mutation réelle Shopify ou Alibaba n’est envoyée pendant la construction de cette version.
