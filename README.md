# Shopify–Alibaba Terminal Orchestrator 2.5.0

Plateforme locale d’automatisation commerciale pour synchroniser un catalogue
Alibaba vers Shopify, calculer le coût rendu et une marge brute cible, recevoir
les commandes Shopify payées, constituer des lots d’approvisionnement, créer et
payer les commandes Alibaba autorisées, synchroniser le suivi, tenir un grand
livre à double entrée et améliorer les décisions avec des modèles incrémentaux
compacts. Depuis la version 1.1.0, l’interface de gestion native C++17 peut
fonctionner sans dépendance IA et sans interface graphique.

La version 2.5.0 conserve intégralement le plan de contrôle 2.4.0 et approfondit les couches encore minces : mémoire SQLite avec TTL, checkpoints atomiques, gouvernance centrale de l’autonomie, transports Shopify/Alibaba instrumentés, décisions financières en Decimal, inventaire multi-emplacement, achats idempotents, fulfillment, retours, chargebacks, marketing, boutique, conformité, observabilité et récupération. Les écritures externes restent bloquées en mode sec et les paiements/publications live exigent toujours les capacités et approbations prévues.

## Contraintes respectées

- Shopify Admin GraphQL `2026-07` est l’interface principale.
- Les webhooks sont validés par HMAC, persistés et dédupliqués avant traitement.
- Les réconciliations périodiques corrigent les événements manqués.
- Alibaba utilise `APP_KEY`, `APP_SECRET`, OAuth et signature de passerelle.
- Les commandes et paiements réels ne s’activent que si les permissions existent.
- Aucun numéro de carte, CVV, NIP ou donnée de piste n’est stocké.
- L’IA est désactivée par défaut. Lorsqu’elle est explicitement activée, elle
  utilise un seul thread et un budget configurable limité à 1 000 Mo.
- Le runtime et les accès HTTP utilisent deux workers au maximum.
- Le mode sûr `APP_DRY_RUN=true` est activé dans `.env.example`.
- SQLite fonctionne en WAL avec tâches persistantes, baux et reprise après panne.
- Le dashboard terminal utilise un rafraîchissement différentiel léger à 2 Hz, sans ajouter de ligne.


## Noyau d’automatisation 2.5.0

Le superviseur planifie 41 opérations canoniques en respectant leur intervalle, une clé d’idempotence par fenêtre, la pression inverse de file et un maximum d’une tâche lourde par cycle sur le profil 2 Go. Les principaux flux sont :

```text
Alibaba discovery -> fournisseur/RFQ -> médias sécurisés -> produit Shopify
Shopify paid order -> risque -> réservation -> intention d’achat -> fournisseur
tracking -> fulfillment Shopify -> client -> retour/remboursement -> comptabilité
```

Les modules de contrôle couvrent notamment :

- prise et normalisation des commandes, chronologie persistante et déduplication ;
- stock disponible/réservé/sécurité/incoming avec allocation transactionnelle ;
- prix historiques, variation, marge minimale et rabais maximum sûr ;
- intention d’achat avec contrainte UNIQUE, transitions conditionnelles et compensation ;
- risques fraude, trésorerie, devise, remboursement, API, livraison et fournisseur ;
- OAuth à usage unique, intégrité de session, verrouillage d’urgence et chaîne d’audit ;
- fournisseurs, RFQ, offres normalisées, échantillons et due diligence ;
- campagnes, contenu, SEO, consentement, canaux de vente et paramètres Shopify ;
- 8 pages terminal fixes et un noyau C++17 avec analyseur de commandes, métriques RAM/CPU et codec IPC.


## Statut de développement par fichier

`PROJECT_TREE.txt` contient désormais une légende et un statut pour chaque fichier :
`✅ COMPLET`, `🧪 TEST`, `🛠 DÉVELOPPÉ`, `🔗 INTÉGRATION`, `📚 DOCUMENTATION`,
`📦 ARTEFACT`, `📁 DONNÉES`, `⚠ À APPROFONDIR` ou `❌ ERREUR`. Le fichier
`PROJECT_FILE_STATUS.json` fournit le même inventaire sous une forme exploitable par les outils.

La commande de régénération est :

```bash
python -m tools.generate_status_tree . --output PROJECT_TREE.txt --json PROJECT_FILE_STATUS.json
```

## Terminal natif Windows MSYS2 MINGW64

Dans un terminal **MSYS2 MINGW64** :

```bash
pacman -S --needed mingw-w64-x86_64-toolchain mingw-w64-x86_64-cmake mingw-w64-x86_64-ninja
bash scripts/windows/build_msys2_mingw64.sh
./build/windows-msys2-mingw64/shopify_alibaba_terminal.exe --dry-run
```

Le terminal natif maintient ses métriques à positions fixes, emploie uniquement
des caractères ASCII sûrs et sépare les compteurs d’actions acceptées, rejetées
et terminées. Sa file de travail est bornée à 64 éléments et applique du
backpressure. Les commandes sensibles restent simulées en dry-run. En mode
`--live`, chaque action financière ou irréversible exige une confirmation exacte
et les montants financiers sont plafonnés par la politique locale.

Le lanceur Python peut également ouvrir l’exécutable déjà compilé :

```bash
python main.py --native-terminal
python main.py --native-live
```

`--native-live` ne contourne jamais les confirmations explicites.

## Plans natifs durables et audit

Le terminal écrit chaque plan par fichier temporaire puis renommage atomique
dans `data/native_plans/pending`. Le runtime vérifie avant import :

- le nom et la taille du fichier ;
- l’ordre et l’unicité des champs ;
- les caractères ASCII et les valeurs numériques ;
- l’identifiant qui doit correspondre au nom de fichier ;
- l’empreinte SHA-256 du contenu canonique.

Les plans valides sont enregistrés dans la table SQLite `native_plans`. Les
plans dry-run et les opérations non sensibles sont classés comme importés. Un
plan live financier ou irréversible est déplacé vers
`data/native_plans/awaiting_approval` et génère obligatoirement une nouvelle
approbation dans SQLite. Il n’est donc pas possible de transformer une simple
confirmation terminal en paiement ou publication directe.

Les plans modifiés, trop grands ou mal formés sont déplacés vers
`data/native_plans/rejected` avec une raison ASCII bornée. Les plans déjà
importés sont reconnus par leur identifiant et ne sont jamais dupliqués.

Chaque événement d’import est ajouté au journal d’audit avec :

- l’empreinte de l’entrée précédente ;
- une sérialisation JSON canonique ;
- une nouvelle empreinte SHA-256.

`python main.py --validate` vérifie toute la chaîne et refuse la validation si
une ancienne entrée a été modifiée.

## Installation Windows

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\windows\install.ps1
Copy-Item .env.example .env
notepad .env
.\scripts\windows\run.ps1
```

## Installation Linux

```bash
chmod +x scripts/linux/*.sh
./scripts/linux/install.sh
cp .env.example .env
nano .env
./scripts/linux/run.sh
```

## Validation

```bash
python main.py --validate
python -m pytest
python -m compileall .
```

## Passage en production

1. Créer l’application Shopify et lui accorder les scopes listés dans
   `config/shopify_scopes.yaml`.
2. Définir un domaine HTTPS public pour les webhooks.
3. Créer et autoriser l’application Alibaba Open Platform.
4. Demander les permissions listées dans `config/alibaba_permissions.yaml`.
5. Enregistrer un moyen de paiement dans le compte Alibaba; ne jamais copier les
   données complètes de carte dans `.env`.
6. Tester toutes les capacités avec les outils du dossier `tools/`.
7. Maintenir `APP_DRY_RUN=true` jusqu’à réussite complète des tests.
8. Approuver explicitement un lot depuis `/api/approvals` lorsque l’approbation
   manuelle est activée.
9. Passer `APP_DRY_RUN=false` uniquement après validation d’un petit lot réel.

## Commandes principales

```bash
python main.py
python main.py --once
python main.py --validate
python main.py --no-dashboard
python main.py --no-api
python main.py --native-terminal
python tools/shopify_scope_inspector.py
python tools/alibaba_permission_probe.py
python scripts/register_shopify_webhooks.py
```

## API locale

- `GET /api/health`
- `GET /api/status`
- `GET /api/dashboard`
- `GET /api/metrics`
- `GET /api/configuration/capabilities`
- `POST /api/webhooks/shopify`
- `GET /api/approvals`
- `POST /api/approvals/{id}/decision`
- Documentation interactive : `/docs`

## Modèle financier

Avec `PRICING_MODE=gross_margin` et
`TARGET_GROSS_MARGIN_PERCENT=50`, le prix est calculé par :

```text
prix = coût_rendu / (1 - 0,50)
```

Le coût rendu inclut le produit, l’expédition, les frais de plateforme, la
réserve de taxes/douanes, la variation de devise et la réserve de remboursement.


https://accounts.shopify.com/lookup?rid=d19ce2af-6f60-4944-b2d7-64bbc8b71d1b&verify=1785470592-5jU3hEmKIiEp514NiVJAHuiAiJur5BaKLf8wB5SiGyA%3D

https://www.shopify.com/ca-fr/partenaires

https://shopify.dev/docs/apps/build/authentication-authorization/access-tokens/online-access-tokens

https://shopify.dev/docs/apps/build/webhooks

https://open.alibaba.com/

https://open.alibaba.com/doc/doc.htm?spm=a2o9m.11193531.0.0.17c9f453PEiTHi&docId=107343&docType=1#/?docId=7

exemple alibaba callback url

https://elit21.com/oauth/alibaba/callback

pour la key base64 utilise ssl

powershell...

openssl rand -base64 32



