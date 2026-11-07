Write-Host "================================="
Write-Host "      RESEARCH AI LAUNCHER"
Write-Host "================================="

$projectPath = Split-Path -Parent $PSScriptRoot

Set-Location $projectPath

if (!(Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Virtual environment missing!"
    exit 1
}

Write-Host "`nStarting ResearchAI..."

& ".venv\Scripts\python.exe" -m backend.main