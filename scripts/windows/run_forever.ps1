$ErrorActionPreference = "Continue"
Set-Location (Split-Path $PSScriptRoot -Parent | Split-Path -Parent)
while ($true) {
  & .\.venv\Scripts\python.exe main.py
  Write-Host "Redémarrage après arrêt inattendu..."
  Start-Sleep -Seconds 10
}
