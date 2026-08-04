$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root
$env:RUNTIME_PROFILE = "live_2gb"
& .\.venv\Scripts\python.exe main.py --validate
if ($LASTEXITCODE -ne 0) { throw "Validation échouée; mode live non lancé." }
& .\.venv\Scripts\python.exe main.py
