$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$Out = Join-Path $Root "data\exports\diagnostics-$Stamp"
New-Item -ItemType Directory -Force $Out | Out-Null
python main.py --validate *> (Join-Path $Out "validation.txt")
python -c "import platform,sys; print(platform.platform()); print(sys.version)" *> (Join-Path $Out "platform.txt")
Get-ChildItem data\logs -ErrorAction SilentlyContinue | Select-Object Name,Length,LastWriteTime | Out-File (Join-Path $Out "logs-index.txt")
Compress-Archive -Path "$Out\*" -DestinationPath "$Out.zip" -Force
Write-Host $Out.zip
