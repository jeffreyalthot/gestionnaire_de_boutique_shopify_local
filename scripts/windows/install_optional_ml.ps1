$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root
if (-not (Test-Path ".venv\Scripts\python.exe")) { throw "Exécutez install_core.ps1 en premier." }
& .\.venv\Scripts\python.exe -m pip install -r requirements-ml-optional.txt
