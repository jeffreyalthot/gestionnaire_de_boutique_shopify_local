$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent | Split-Path -Parent)
& .\.venv\Scripts\python.exe main.py
