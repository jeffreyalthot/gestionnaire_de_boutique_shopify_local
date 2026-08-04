@echo off
setlocal EnableExtensions

cd /d "%~dp0"

echo [1/5] Verification du dossier racine...
if not exist "CMakeLists.txt" (
    echo ERREUR: CMakeLists.txt introuvable.
    echo Placez ce fichier .bat dans la racine du projet 2.5.0.
    pause
    exit /b 1
)

echo [2/5] Remise a l'heure des fichiers CMake...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$now = Get-Date; " ^
  "Get-ChildItem -LiteralPath . -Recurse -File -Include CMakeLists.txt,*.cmake,CMakePresets.json,CMakeUserPresets.json | ForEach-Object { $_.CreationTime=$now; $_.LastWriteTime=$now; $_.LastAccessTime=$now }"

if errorlevel 1 (
    echo ERREUR: impossible de corriger les horodatages.
    pause
    exit /b 1
)

echo [3/5] Suppression de l'ancien dossier build...
if exist "build" rmdir /s /q "build"

echo [4/5] Configuration CMake...
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
if errorlevel 1 (
    echo ERREUR: configuration CMake echouee.
    pause
    exit /b 1
)

echo [5/5] Compilation Ninja...
cmake --build build --parallel 2
if errorlevel 1 (
    echo ERREUR: compilation echouee.
    pause
    exit /b 1
)

echo.
echo BUILD TERMINE AVEC SUCCES.
pause
endlocal
