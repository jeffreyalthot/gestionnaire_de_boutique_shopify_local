# Cycle du runtime

Démarrage : chargement de `.env`, création des répertoires, migration SQLite, contrôles de sécurité, lancement des workers, du planificateur, du dashboard et de FastAPI. Arrêt : signal, fermeture des consommateurs, annulation contrôlée et fermeture HTTP.
