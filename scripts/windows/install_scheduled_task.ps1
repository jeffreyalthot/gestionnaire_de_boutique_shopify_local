$Root = Split-Path $PSScriptRoot -Parent | Split-Path -Parent
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$Root\scripts\windows\run_forever.ps1`""
$Trigger = New-ScheduledTaskTrigger -AtStartup
$Settings = New-ScheduledTaskSettingsSet -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1) -ExecutionTimeLimit (New-TimeSpan -Days 3650)
Register-ScheduledTask -TaskName "ShopifyAlibabaAIOrchestrator" -Action $Action -Trigger $Trigger -Settings $Settings -RunLevel Highest -Force
