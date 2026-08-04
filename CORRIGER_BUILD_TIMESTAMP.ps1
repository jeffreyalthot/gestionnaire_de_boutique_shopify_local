$ErrorActionPreference = "Stop"

Set-Location -LiteralPath $PSScriptRoot

if (-not (Test-Path -LiteralPath ".\CMakeLists.txt")) {
    throw "CMakeLists.txt introuvable. Placez ce script dans la racine du projet 2.5.0."
}

Write-Host "[1/4] Correction des horodatages CMake..."
$now = Get-Date

Get-ChildItem -LiteralPath . -Recurse -File |
    Where-Object {
        $_.Name -eq "CMakeLists.txt" -or
        $_.Extension -eq ".cmake" -or
        $_.Name -eq "CMakePresets.json" -or
        $_.Name -eq "CMakeUserPresets.json"
    } |
    ForEach-Object {
        $_.CreationTime = $now
        $_.LastWriteTime = $now
        $_.LastAccessTime = $now
    }

Write-Host "[2/4] Suppression de l'ancien build..."
if (Test-Path -LiteralPath ".\build") {
    Remove-Item -LiteralPath ".\build" -Recurse -Force
}

Write-Host "[3/4] Configuration..."
& cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
if ($LASTEXITCODE -ne 0) { throw "Configuration CMake echouee." }

Write-Host "[4/4] Compilation..."
& cmake --build build --parallel 2
if ($LASTEXITCODE -ne 0) { throw "Compilation Ninja echouee." }

Write-Host "BUILD TERMINE AVEC SUCCES."
