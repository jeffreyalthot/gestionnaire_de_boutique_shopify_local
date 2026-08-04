$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw "Python 3.11+ est requis." }
if (-not (Test-Path ".venv")) { python -m venv .venv }
& .\.venv\Scripts\python.exe -m pip install --upgrade pip wheel
& .\.venv\Scripts\python.exe -m pip install -r requirements-windows-lite.txt
& .\.venv\Scripts\python.exe scripts\initialize_database.py
Write-Host "Installation core terminée. Copiez .env.lite.example vers .env puis validez."
