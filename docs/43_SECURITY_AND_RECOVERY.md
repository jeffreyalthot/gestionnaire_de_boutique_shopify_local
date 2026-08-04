# Sécurité et récupération

- OAuth : état aléatoire, stockage SHA-256, expiration et consommation unique.
- Audit : chaînage SHA-256 et vérification complète au démarrage.
- Média : garde SSRF, signature de format, taille maximale et empreinte SHA-256.
- Runtime : verrouillage d’urgence impossible à lever sans autorisation explicite.
- SQLite : WAL, transactions courtes, quick-check, baux expirés et reprise des tâches.
- Secrets : analyse des sources texte uniquement; binaires, builds, caches et modèles sont exclus.
- PII : conservation configurable et script explicite de purge avec audit.
