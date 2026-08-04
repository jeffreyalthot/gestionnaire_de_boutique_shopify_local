# Version 2.4.0

La version 2.4.0 approfondit le code source 2.3.0 sans supprimer ses modules ni modifier son architecture canonique.

## Développements majeurs

- autonomie centralisée avec décisions de capacité, risque, confiance, budget et verrouillage d’urgence ;
- mémoire IA SQLite avec TTL, historique et tags ;
- checkpoints atomiques compressés avec SHA-256 et rétention déterministe ;
- transports Shopify GraphQL et Alibaba instrumentés, bornés et repris ;
- calculs financiers Decimal, réserves et profit par dimension ;
- inventaire multi-emplacement, réservation, backorder, preorder et détection de données périmées ;
- achat fournisseur idempotent, suivi de paiement, annulation et compensation ;
- fulfillment, notifications, retours, chargebacks et service client ;
- marketing, SEO, boutique, fiscalité, conformité et intelligence fournisseur ;
- observabilité, incidents, rapports atomiques, workers bornés et santé SQLite ;
- terminal à lignes fixes préservé.

## Sécurité opérationnelle

Le mode sec demeure la configuration par défaut. Les paiements, remboursements, publications et autres mutations externes réelles restent soumis aux capacités API, aux politiques locales et aux approbations prévues.
