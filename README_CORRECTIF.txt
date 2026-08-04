CORRECTIF HORODATAGE CMAKE — VERSION 2.5.0

Cause confirmée
---------------
Ninja indique que build.ninja est plus ancien que CMakeLists.txt après chaque
régénération. Le fichier CMakeLists.txt conserve donc une date future ou une date
incompatible avec l'horloge utilisée pour générer build.ninja.

Installation
------------
1. Extraire les deux scripts à la RACINE du projet, à côté de CMakeLists.txt.
2. Fermer les terminaux, IDE et outils qui surveillent le projet.
3. Exécuter CORRIGER_BUILD_TIMESTAMP.bat.
4. Le script corrige les dates de tous les fichiers CMake, supprime build,
   reconfigure avec Ninja puis compile avec 2 tâches.

Alternative PowerShell
----------------------
powershell -ExecutionPolicy Bypass -File .\CORRIGER_BUILD_TIMESTAMP.ps1

Important
---------
Si la date redevient future immédiatement après ce script, corriger l'heure et
le fuseau horaire de Windows, puis désactiver temporairement tout outil de
synchronisation qui restaure les métadonnées du fichier.
