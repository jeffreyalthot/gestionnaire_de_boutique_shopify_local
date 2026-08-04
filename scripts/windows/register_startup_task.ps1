param([string]$ProjectRoot=(Resolve-Path "$PSScriptRoot\..\.."))
$Action=New-ScheduledTaskAction -Execute "$ProjectRoot\.venv\Scripts\python.exe" -Argument 'main.py --no-api' -WorkingDirectory $ProjectRoot
$Trigger=New-ScheduledTaskTrigger -AtLogOn
$Settings=New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)
Register-ScheduledTask -TaskName 'ShopifyAlibabaOrchestrator' -Action $Action -Trigger $Trigger -Settings $Settings -Description 'Gestionnaire terminal Shopify Alibaba' -Force
