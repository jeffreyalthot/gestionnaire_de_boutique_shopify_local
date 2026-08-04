$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root
$env:RUNTIME_PROFILE = "lite_2gb"
$env:AI_ENABLED = "false"
$env:APP_DRY_RUN = "true"
& .\.venv\Scripts\python.exe main.py
