# Rapport de développement — Shopify–Alibaba 2.5.0

## Résumé exécutif

La version 2.5.0 approfondit la distribution 2.4.0 sans supprimer, déplacer ou remplacer son architecture canonique. Le gestionnaire terminal à lignes fixes reste l’unique propriétaire de la console; les workers, transports et workflows publient leurs états par des structures bornées au lieu d’écrire directement dans le terminal.

## Préservation et volume

- Fichiers de référence 2.4.0 : **2171**.
- Fichiers de référence préservés : **2171**.
- Fichiers supprimés : **0**.
- Nouveaux fichiers 2.5.0 : **16**.
- Fichiers antérieurs modifiés : **247**.
- Fichiers finaux : **2187**.
- Modules Python : **1 729** (environ 37 297 lignes).
- Sources C++ : **58**; en-têtes : **49**.

## Validation automatisée

- **431 tests Python réussis**.
- Compilation Python complète réussie.
- Build C++17 Release réussi avec un parallélisme limité à deux tâches.
- **15 tests C++ sur 15 réussis**.
- Validation de configuration : `ok: true` en mode sec.
- Cycle sec observé : 41 opérations planifiées, 27 acceptées, 14 différées, 26 terminées pendant la fenêtre observée, 0 rejetée et 0 échouée.
- Pic mémoire observé : environ **232,7 Mio**.
- Wheel 2.5.0 vérifié : 1 721 entrées, 69 opérations GraphQL Shopify, 8 contrats Alibaba et 89 fichiers YAML.

## Développement fonctionnel

### Automatisation et décisions

- noyau d’autonomie tenant compte des capacités, du mode, du risque, de la confiance, du montant, de la pression CPU/RAM et du verrouillage d’urgence;
- workflows auditables avec délais, reprises bornées, idempotence, checkpoints et compensations inverses;
- politiques composables avec historique, statistiques, budget de violations et décision explicable;
- machines d’état gardées, terminales, introspectables et entièrement auditées.

### Shopify et Alibaba

- transports instrumentés avec durée, identifiants de requête, coûts GraphQL, débit, reprises et diagnostics;
- webhooks bornés en taille/profondeur, normalisés récursivement et protégés contre les doublons et événements hors ordre;
- mappers Shopify complets pour GID, montants `Decimal`, pagination, variantes, inventaire, commandes, clients, fulfillments et remboursements;
- méthodes Alibaba validées, normalisées, empreintées et mesurées;
- réconciliation profonde bidirectionnelle avec tolérances numériques, différences bornées et checkpoints persistants.

### Runtime faible mémoire

- caches, mémoires et files bornés;
- stockage de caractéristiques versionné avec comparaison-et-échange;
- modèles locaux en flux, explicables et sérialisables, dont un détecteur d’anomalies pur Python;
- verrous de processus récupérables, client HTTP limité, reprises sélectives et tâches versionnées;
- rapports, panneaux et métriques à historique borné;
- widgets C++ redimensionnables respectant le contrat strict d’absence de défilement.

## Statuts du TREE

- ✅ COMPLET : **182**.
- 🛠 DÉVELOPPÉ : **1 346**.
- 🔗 INTÉGRATION : **350**.
- 🧪 TEST : **183**.
- 📚 DOCUMENTATION : **94**.
- 📦 ARTEFACT : **5**.
- 📁 DONNÉES : **27**.
- ⚠ À APPROFONDIR : **0**.
- ❌ ERREUR : **0**.

## Limites de validation

Les validations Shopify, Alibaba, paiements, remboursements, publications, fulfillments et commandes fournisseur ont été exécutées en mode sec ou avec des transports simulés. Aucune mutation externe réelle n’a été envoyée. La construction du wheel a été effectuée sans isolation de build parce que l’index de paquets de l’environnement ne permettait pas de retélécharger la version demandée de `setuptools`; le wheel a ensuite été installé dans une cible distincte et ses imports critiques ont été vérifiés avec les dépendances déjà validées de l’hôte.
