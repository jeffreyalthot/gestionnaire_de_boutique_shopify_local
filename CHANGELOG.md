## 2.5.0 — 2026-07-30

- Réconciliateurs profonds et persistants avec écarts imbriqués, doublons et tolérances.
- Rapports structurés avec empreinte, limites, filtres et exports atomiques.
- Workers, workflows et méthodes Alibaba instrumentés et bornés.
- Agents métier spécialisés avec historique, scores et recommandations explicables.
- Terminal C++ enrichi : buffers redimensionnables, tables, tendances, pages et suppression ANSI.
- Webhooks Shopify validés récursivement avec empreinte complète et métadonnées de livraison.
- Mappers Shopify robustes pour produits, variantes, commandes, clients, inventaire, fulfillment et remboursements.
- API opérateur renforcée, tâches versionnées, verrous récupérables et reprises sélectives.
- Machines d’état auditables, événements de domaine versionnés et modèles faibles ressources sans dépendance lourde obligatoire.
- 431 tests Python et 15 tests C++ au moment de la publication.

## 2.4.0 — 2026-07-30
- Approfondissement massif des services IA légers, financiers, catalogue, commandes, fournisseurs, fulfillment, retours, sécurité, localisation, observabilité et runtime faible mémoire.
- Ajout de décisions explicables, persistance TTL, checkpoints SHA-256, idempotence des paiements/achats, compensation, sélection transport multi-critères et suivi des chargebacks.
- Renforcement du gouverneur de ressources Windows 2 Go, des diagnostics SQLite, des tâches manquées, des caches, des alertes et du terminal fixe.
- Ajout de plus de 100 tests ciblés 2.4.0 en conservant tous les tests historiques.

## 2.3.0
- Agents déterministes explicables, webhooks Shopify routés, canaux, boutique, RFQ, taxes, qualité et TREE statué.

# Journal des versions

## 2.2.0 — 2026-07-30
- Ajout d’un plan de contrôle runtime : registre de services, bus de commandes/requêtes/événements, santé agrégée, snapshots, récupération et routage des exceptions.
- Passage à 37 opérations périodiques idempotentes avec intervalles, backpressure, budget CPU/RAM et une seule tâche lourde par cycle.
- Ajout des tables SQLite pour positions de stock, intentions d’achat, chronologies de commande, historiques de prix, décisions de risque, OAuth et versions de justificatifs.
- Ajout du chemin commande complet : intake, validation, risque, réservation atomique anti-survente, découpage fournisseur, intention d’achat et compensation.
- Ajout de la tarification protégée par marge, de l’historique et des contrôles de rabais, transport, devise et prix fournisseur.
- Ajout de l’intelligence fournisseur, RFQ, due diligence, échantillons, qualité, retours, remboursements, fiscalité, marketing, SEO, localisation, canaux de vente et gestion de boutique.
- Extension du terminal C++17 : registre/analyseur de commandes, codec IPC, propriétaire de sortie, métriques RAM/CPU, mise en page validée, éditeur et barre de progression.
- Correction du scanner de secrets afin d’ignorer les artefacts binaires et les caches sans ignorer les sources.
- Ajout des profils/scripts Windows 2 Go, diagnostics, maintenance, génération de manifeste et vérification de livraison.
- Validation : 128 tests Python, 4 tests natifs, compilation Python complète, validation dry-run et cycle de 37 opérations.

## 1.2.0 — 2026-07-29
- Remplacement de la temporisation simulée du terminal natif par une
  persistance atomique réelle des plans dans `data/native_plans/pending`.
- Ajout d’une implémentation SHA-256 C++17 sans dépendance externe, validée
  avec les vecteurs officiels pour `abc` et l’entrée vide.
- Ajout d’un format de plan ASCII strict, borné à 8 192 octets, signé par
  empreinte SHA-256 et protégé contre les traversées de chemin.
- Ajout du pont runtime `NativePlanBridge` : validation stricte, import
  idempotent dans SQLite, quarantaine des plans invalides et récupération
  automatique des fichiers laissés en attente après une interruption.
- Ajout d’une seconde approbation runtime obligatoire pour les plans live
  financiers ou irréversibles, même s’ils ont été confirmés dans le terminal.
- Migration SQLite additive vers le schéma 2 avec table `native_plans`.
- Transformation du journal d’audit en chaîne SHA-256 vérifiable, avec
  migration et chaînage des anciennes entrées.
- Ajout de la vérification de la chaîne d’audit aux contrôles de démarrage et
  au tableau d’état du runtime.
- Correction du contrôle de démarrage pour respecter le plafond IA configuré
  de 1 000 Mo.
- Ajout de 8 nouveaux contrôles C++ et de 5 tests Python autonomes portant sur
  la migration, la falsification, l’idempotence et les approbations.

## 1.1.0 — 2026-07-28
- Ajout d’un noyau terminal natif C++17 compilable sous MSYS2 MINGW64.
- Ajout d’une politique déterministe dry-run/live avec approbation obligatoire
  pour les actions irréversibles et financières.
- Ajout d’une file bornée avec backpressure et deux workers maximum.
- Ajout d’un tableau de bord terminal ASCII à positions fixes avec compteurs
  acceptés, rejetés, terminés et profondeur de file.
- Ajout des presets CMake, du script de build Windows et de tests C++ sans
  dépendance externe.
- L’IA et l’apprentissage en ligne sont maintenant désactivés par défaut.
- La concurrence HTTP est plafonnée à deux et le budget IA configurable à
  1 000 Mo maximum.
- Intégration du terminal natif dans `main.py` via `--native-terminal`.

## 1.0.0 — 2026-07-24
- Première livraison complète.
- Intégrations Shopify GraphQL et Alibaba Open Platform.
- Runtime asyncio, file durable SQLite, dashboard, comptabilité et IA locale.

## 2.2.0 - 2026-07-30

- Approfondissement des calculs financiers, caractéristiques de décision et politiques d'autonomie.
- Cache LRU/TTL borné et verrouillage interprocessus robuste.
- Réception Shopify enrichie avec métadonnées, HMAC strict, ordre des événements et réconciliation persistante.
- Gestion adaptative du budget GraphQL et pagination défensive.
- Schémas API, inventaire, conformité, SEO et marketing renforcés.
